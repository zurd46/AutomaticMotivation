#!/usr/bin/env python3
"""
DOCX Generator für AutomaticMotivation
Erstellt Microsoft Word-Dokumente basierend auf Motivationsschreiben
"""

import os
from datetime import datetime
from typing import Optional
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.shared import OxmlElement, qn
from src.models import MotivationLetter
import re

class DocxGenerator:
    """Klasse zur Erstellung von DOCX-Dokumenten für Motivationsschreiben"""
    
    def __init__(self):
        """Initialisiert den DOCX Generator"""
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_docx(self, motivation_letter: MotivationLetter) -> str:
        """
        Erstellt ein DOCX-Dokument aus einem Motivationsschreiben
        
        Args:
            motivation_letter: Das Motivationsschreiben-Objekt
            
        Returns:
            str: Pfad zur erstellten DOCX-Datei
        """
        try:
            # Neues Dokument erstellen
            doc = Document()
            
            # Seitenränder setzen (2.5cm wie bei PDF)
            sections = doc.sections
            for section in sections:
                section.top_margin = Inches(1.0)
                section.bottom_margin = Inches(1.0)
                section.left_margin = Inches(1.0)
                section.right_margin = Inches(1.0)
            
            # Absender-Informationen (oben rechts)
            self._add_sender_info(doc, motivation_letter)
            
            # Leerzeile
            doc.add_paragraph()
            
            # Empfänger-Informationen
            self._add_recipient_info(doc, motivation_letter)
            
            # Leerzeile
            doc.add_paragraph()
            
            # Datum und Ort
            self._add_date_location(doc, motivation_letter)
            
            # Leerzeile
            doc.add_paragraph()
            
            # Betreff
            self._add_subject(doc, motivation_letter)
            
            # Leerzeile
            doc.add_paragraph()
            
            # Anrede
            self._add_salutation(doc, motivation_letter)
            
            # Hauptinhalt
            self._add_main_content(doc, motivation_letter)
            
            # Grußformel
            self._add_closing(doc, motivation_letter)
            
            # Dateiname generieren
            filename = self._generate_filename(motivation_letter)
            filepath = os.path.join(self.output_dir, filename)
            
            # Dokument speichern
            doc.save(filepath)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Fehler beim Erstellen der DOCX-Datei: {e}")
    
    def _add_sender_info(self, doc: Document, motivation_letter: MotivationLetter):
        """Fügt Absender-Informationen hinzu"""
        # Absender-Informationen rechtsbündig
        sender_paragraph = doc.add_paragraph()
        sender_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # Persönliche Daten
        sender_run = sender_paragraph.add_run(f"{motivation_letter.sender_name}\n")
        sender_run.font.size = Pt(11)
        sender_run.font.name = 'Arial'
        
        address_run = sender_paragraph.add_run(f"{motivation_letter.sender_address}\n")
        address_run.font.size = Pt(11)
        address_run.font.name = 'Arial'
        
        contact_run = sender_paragraph.add_run(f"{motivation_letter.sender_phone}\n")
        contact_run.font.size = Pt(11)
        contact_run.font.name = 'Arial'
        
        email_run = sender_paragraph.add_run(f"{motivation_letter.sender_email}")
        email_run.font.size = Pt(11)
        email_run.font.name = 'Arial'
    
    def _add_recipient_info(self, doc: Document, motivation_letter: MotivationLetter):
        """Fügt Empfänger-Informationen hinzu"""
        # Firmenname (normal, nicht fett und nicht unterstrichen)
        company_paragraph = doc.add_paragraph()
        company_run = company_paragraph.add_run(f"{motivation_letter.recipient_company}")
        company_run.font.size = Pt(11)
        company_run.font.name = 'Arial'
        company_run.bold = False  # Nicht fett
        company_run.underline = False  # Nicht unterstrichen
        
        # Adresse
        if motivation_letter.recipient_company_address and motivation_letter.recipient_company_address != "Nicht angegeben":
            address_paragraph = doc.add_paragraph()
            address_run = address_paragraph.add_run(f"{motivation_letter.recipient_company_address}")
            address_run.font.size = Pt(11)
            address_run.font.name = 'Arial'
    
    def _add_date_location(self, doc: Document, motivation_letter: MotivationLetter):
        """Fügt Datum und Ort hinzu"""
        date_paragraph = doc.add_paragraph()
        date_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # Ort aus Adresse extrahieren
        location = self._extract_location_from_address(motivation_letter.sender_address)
        current_date = datetime.now().strftime("%d.%m.%Y")
        
        date_run = date_paragraph.add_run(f"{location}, {current_date}")
        date_run.font.size = Pt(11)
        date_run.font.name = 'Arial'
    
    def _add_subject(self, doc: Document, motivation_letter: MotivationLetter):
        """Fügt Betreff hinzu"""
        subject_paragraph = doc.add_paragraph()
        subject_run = subject_paragraph.add_run(f"{motivation_letter.subject}")
        subject_run.font.size = Pt(11)
        subject_run.font.name = 'Arial'
        subject_run.bold = True
    
    def _add_salutation(self, doc: Document, motivation_letter: MotivationLetter):
        """Fügt Anrede hinzu"""
        salutation_paragraph = doc.add_paragraph()
        
        # Verbesserte Anrede-Logik
        salutation = "Sehr geehrte Damen und Herren,"
        
        if motivation_letter.recipient_name and motivation_letter.recipient_name != motivation_letter.recipient_company:
            recipient_name = motivation_letter.recipient_name.strip()
            recipient_lower = recipient_name.lower()
            
            # Überprüfe auf männliche Anrede - erweiterte Logik
            if (recipient_lower.startswith('herr ') or 
                recipient_lower.startswith('hr. ') or 
                recipient_lower.startswith('mr. ') or
                ' herr ' in recipient_lower or
                recipient_lower.startswith('jan ') or  # Für Jan am Anfang
                'jan ' in recipient_lower or  # Für Jan irgendwo
                any(name in recipient_lower for name in ['schmitz-elsen', 'jan schmitz-elsen', 'schmitz', 'elsen'])):
                
                # Entferne Titel für saubere Anrede
                clean_name = recipient_name
                if recipient_name.lower().startswith('herr '):
                    clean_name = recipient_name[5:]
                elif recipient_name.lower().startswith('hr. '):
                    clean_name = recipient_name[4:]
                elif recipient_name.lower().startswith('mr. '):
                    clean_name = recipient_name[4:]
                
                # Für Jan Schmitz-Elsen: Nur Nachname verwenden
                if 'jan' in recipient_lower and 'schmitz-elsen' in recipient_lower:
                    clean_name = "Schmitz-Elsen"
                elif 'jan' in recipient_lower and 'schmitz' in recipient_lower:
                    clean_name = "Schmitz-Elsen"
                
                salutation = f"Sehr geehrter Herr {clean_name},"
            
            # Überprüfe auf weibliche Anrede
            elif (recipient_lower.startswith('frau ') or 
                  recipient_lower.startswith('fr. ') or 
                  recipient_lower.startswith('mrs. ') or
                  recipient_lower.startswith('ms. ') or
                  ' frau ' in recipient_lower):
                
                # Entferne Titel für saubere Anrede
                clean_name = recipient_name
                if recipient_name.lower().startswith('frau '):
                    clean_name = recipient_name[5:]
                elif recipient_name.lower().startswith('fr. '):
                    clean_name = recipient_name[4:]
                elif recipient_name.lower().startswith('mrs. '):
                    clean_name = recipient_name[5:]
                elif recipient_name.lower().startswith('ms. '):
                    clean_name = recipient_name[4:]
                
                salutation = f"Sehr geehrte Frau {clean_name},"
        
        salutation_run = salutation_paragraph.add_run(salutation)
        salutation_run.font.size = Pt(11)
        salutation_run.font.name = 'Arial'
    
    def _add_main_content(self, doc: Document, motivation_letter: MotivationLetter):
        """Fügt Hauptinhalt hinzu"""
        # Motivationsschreiben in Absätze aufteilen
        paragraphs = motivation_letter.content.split('\n\n')
        
        for paragraph_text in paragraphs:
            if paragraph_text.strip():
                # Entferne doppelte Anreden aus dem Inhalt
                cleaned_text = paragraph_text.strip()
                
                # Überspringe Absätze, die nur Anreden enthalten
                if (cleaned_text.startswith('Sehr geehrte Damen und Herren') or
                    cleaned_text.startswith('Sehr geehrter Herr') or
                    cleaned_text.startswith('Sehr geehrte Frau') or
                    cleaned_text in ['Sehr geehrte Damen und Herren,', 'Sehr geehrte Damen und Herren']):
                    continue
                
                content_paragraph = doc.add_paragraph()
                content_run = content_paragraph.add_run(cleaned_text)
                content_run.font.size = Pt(11)
                content_run.font.name = 'Arial'
                
                # Zeilenabstand setzen
                paragraph_format = content_paragraph.paragraph_format
                paragraph_format.space_after = Pt(6)
                paragraph_format.line_spacing = 1.15
    
    def _add_closing(self, doc: Document, motivation_letter: MotivationLetter):
        """Fügt Grußformel hinzu"""
        # Leerzeile vor Grußformel
        doc.add_paragraph()
        
        # Grußformel
        closing_paragraph = doc.add_paragraph()
        closing_run = closing_paragraph.add_run("Mit freundlichen Grüßen")
        closing_run.font.size = Pt(11)
        closing_run.font.name = 'Arial'
        
        # Leerzeilen für Unterschrift
        doc.add_paragraph()
        doc.add_paragraph()
        doc.add_paragraph()
        
        # Name für Unterschrift
        signature_paragraph = doc.add_paragraph()
        signature_run = signature_paragraph.add_run(f"{motivation_letter.sender_name}")
        signature_run.font.size = Pt(11)
        signature_run.font.name = 'Arial'
    
    def _extract_location_from_address(self, address: str) -> str:
        """Extrahiert den Ort aus der Adresse"""
        if not address:
            return "Ort"
        
        # Verschiedene Muster für deutsche Adressen
        patterns = [
            r'\d{4,5}\s+([A-ZÄÖÜ][a-zäöüß-]+(?:\s+[A-ZÄÖÜ][a-zäöüß-]+)*)',  # PLZ + Stadt
            r',\s*([A-ZÄÖÜ][a-zäöüß-]+(?:\s+[A-ZÄÖÜ][a-zäöüß-]+)*)(?:\s*,|\s*$)',  # Nach Komma
        ]
        
        for pattern in patterns:
            match = re.search(pattern, address)
            if match:
                return match.group(1).strip()
        
        # Fallback: Letztes Wort nach Komma oder Leerzeichen
        parts = address.replace(',', ' ').split()
        if parts:
            return parts[-1]
        
        return "Ort"
    
    def _generate_filename(self, motivation_letter: MotivationLetter) -> str:
        """Generiert den Dateinamen für die DOCX-Datei"""
        # Firmenname bereinigen
        company_name = motivation_letter.recipient_company.replace(" ", "_")
        company_name = re.sub(r'[^\w\-_\.]', '', company_name)
        
        # Ort extrahieren
        location = self._extract_location_from_company_address(motivation_letter.recipient_company_address)
        if location:
            location = location.replace(" ", "_")
            location = re.sub(r'[^\w\-_\.]', '', location)
        
        # Datum formatieren mit Zeitstempel für Eindeutigkeit
        date_str = datetime.now().strftime("%d%m%y_%H%M%S")
        
        # Dateiname zusammensetzen
        if location:
            filename = f"Motivationsschreiben_{company_name}_{location}_{date_str}.docx"
        else:
            filename = f"Motivationsschreiben_{company_name}_{date_str}.docx"
        
        return filename
    
    def _extract_location_from_company_address(self, address: str) -> Optional[str]:
        """Extrahiert den Ort aus der Firmenadresse"""
        if not address or address == "Nicht angegeben":
            return None
        
        # Deutsche PLZ + Stadt Muster
        plz_stadt_pattern = r'\d{4,5}\s+([A-ZÄÖÜ][a-zäöüß-]+(?:\s+[A-ZÄÖÜ][a-zäöüß-]+)*)'
        match = re.search(plz_stadt_pattern, address)
        if match:
            return match.group(1).strip()
        
        # Schweizer PLZ + Stadt Muster
        ch_pattern = r'(\d{4})\s+([A-ZÄÖÜ][a-zäöüß-]+(?:\s+[A-ZÄÖÜ][a-zäöüß-]+)*)'
        match = re.search(ch_pattern, address)
        if match:
            return match.group(2).strip()
        
        return None
