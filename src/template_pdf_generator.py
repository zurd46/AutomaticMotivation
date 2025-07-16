import os
import json
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pdfplumber
import PyPDF2
import logging
from src.models import MotivationLetter
from config.config import Config

logger = logging.getLogger(__name__)

class TemplateBasedPDFGenerator:
    """Erweiterte PDF-Generator Klasse mit Template-Unterstützung"""
    
    def __init__(self, template_path: str = None):
        self.template_path = template_path or "templates/template.pdf"
        self.page_width, self.page_height = A4
        self.styles = getSampleStyleSheet()
        self.template_analysis = None
        self._setup_styles()
        
        # Template analysieren falls vorhanden
        if os.path.exists(self.template_path):
            self.template_analysis = self.analyze_template()
    
    def _setup_styles(self):
        """Richtet Styles basierend auf Template ein"""
        # Basis-Styles für deutsches Motivationsschreiben
        
        # Absender-Style (oben rechts)
        self.styles.add(ParagraphStyle(
            name='Sender',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_RIGHT,
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        # Empfänger-Style (links)
        self.styles.add(ParagraphStyle(
            name='Recipient',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=12,
            spaceBefore=24,
            fontName='Helvetica'
        ))
        
        # Datum-Style (rechts)
        self.styles.add(ParagraphStyle(
            name='Date',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_RIGHT,
            spaceAfter=24,
            fontName='Helvetica'
        ))
        
        # Betreff-Style (fett)
        self.styles.add(ParagraphStyle(
            name='Subject',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_LEFT,
            spaceAfter=18,
            fontName='Helvetica-Bold'
        ))
        
        # Anrede-Style
        self.styles.add(ParagraphStyle(
            name='Salutation',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=12,
            fontName='Helvetica'
        ))
        
        # Haupttext-Style (Blocksatz)
        self.styles.add(ParagraphStyle(
            name='MainText',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16,
            fontName='Helvetica'
        ))
        
        # Grußformel-Style
        self.styles.add(ParagraphStyle(
            name='Closing',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=36,
            spaceBefore=12,
            fontName='Helvetica'
        ))
        
        # Signatur-Style
        self.styles.add(ParagraphStyle(
            name='Signature',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            fontName='Helvetica'
        ))
    
    def analyze_template(self) -> dict:
        """Analysiert das PDF-Template und extrahiert Layout-Informationen"""
        try:
            if not os.path.exists(self.template_path):
                logger.warning(f"Template nicht gefunden: {self.template_path}")
                return None
                
            analysis = {
                "pages": 0,
                "text_blocks": [],
                "layout": {},
                "fonts": [],
                "margins": {},
                "elements": []
            }
            
            with pdfplumber.open(self.template_path) as pdf:
                analysis["pages"] = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages):
                    # Seitenabmessungen
                    analysis["layout"][f"page_{page_num}"] = {
                        "width": page.width,
                        "height": page.height,
                        "bbox": page.bbox
                    }
                    
                    # Text extrahieren mit Positionen
                    chars = page.chars
                    if chars:
                        for char in chars[:10]:  # Nur erste 10 Zeichen für Analyse
                            analysis["text_blocks"].append({
                                "text": char.get("text", ""),
                                "x": char.get("x0", 0),
                                "y": char.get("y0", 0),
                                "fontname": char.get("fontname", ""),
                                "size": char.get("size", 0)
                            })
                    
                    # Textblöcke extrahieren
                    text = page.extract_text()
                    if text:
                        analysis["elements"].append({
                            "type": "text",
                            "content": text[:200],  # Erste 200 Zeichen
                            "page": page_num
                        })
            
            logger.info(f"Template analysiert: {analysis['pages']} Seiten")
            return analysis
            
        except Exception as e:
            logger.error(f"Fehler bei Template-Analyse: {e}")
            return None
    
    def create_pdf_from_template(self, motivation_letter: MotivationLetter, 
                               output_dir: str = "output") -> str:
        """Erstellt PDF basierend auf Template-Analyse"""
        try:
            # Ausgabeordner erstellen
            os.makedirs(output_dir, exist_ok=True)
            
            # Dateiname generieren
            date_str = datetime.now().strftime("%d%m%y")  # Format: TTMMJJ
            
            # Verwende Firmenname, falls vorhanden, sonst Empfängername
            if motivation_letter.recipient_company and motivation_letter.recipient_company != "Nicht angegeben":
                company_name = motivation_letter.recipient_company
            else:
                company_name = motivation_letter.recipient_name
            
            # Bereinige Firmennamen für Dateinamen
            company_name = company_name.replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("?", "_").replace("*", "_").replace("|", "_").replace("<", "_").replace(">", "_").replace('"', "_")
            
            # Extrahiere Ort aus der Firmenadresse
            location = ""
            if motivation_letter.recipient_company_address and motivation_letter.recipient_company_address != "Nicht angegeben":
                address = motivation_letter.recipient_company_address
                
                # Verschiedene Parsing-Strategien versuchen
                address_parts = address.split(", ")
                
                for part in address_parts:
                    part = part.strip()
                    
                    # Prüfe ob Teil eine Stadt sein könnte
                    if part:
                        # Strategie 1: Suche nach PLZ + Stadt Muster (z.B. "4052 Basel")
                        if " " in part:
                            words = part.split()
                            # Wenn erste Wort eine PLZ ist (4-5 Ziffern), nehme den Rest als Stadt
                            if len(words) >= 2 and words[0].isdigit() and len(words[0]) >= 4:
                                location = " ".join(words[1:])
                                break
                        
                        # Strategie 2: Prüfe ob Teil nur eine Stadt ist (keine Straße, keine PLZ)
                        if (not part[0].isdigit() and  # Keine PLZ/Hausnummer
                            not any(street_word in part.lower() for street_word in ["platz", "strasse", "straße", "weg", "gasse", "allee"]) and  # Keine Straßennamen
                            part.lower() not in ["schweiz", "switzerland", "ch", "deutschland", "germany", "österreich", "austria"]):  # Nicht Land
                            location = part
                            break
            
            # Bereinige Ort für Dateinamen
            if location:
                location = location.replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("?", "_").replace("*", "_").replace("|", "_").replace("<", "_").replace(">", "_").replace('"', "_")
                filename = f"Motivationsschreiben_{company_name}_{location}_{date_str}.pdf"
            else:
                filename = f"Motivationsschreiben_{company_name}_{date_str}.pdf"
                
            filepath = os.path.join(output_dir, filename)
            
            # PDF erstellen
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # Inhalt basierend auf deutschem Standard erstellen
            story = []
            
            # 1. Absender (oben rechts - exaktes Format)
            sender_text = f"""
            {motivation_letter.sender_name}<br/>
            Hinterdorfstrasse 12<br/>
            6235 Winikon<br/>
            Tel: {motivation_letter.sender_phone}<br/>
            E-Mail: {motivation_letter.sender_email}
            """
            story.append(Paragraph(sender_text, self.styles['Sender']))
            story.append(Spacer(1, 12))
            
            # 2. Empfänger (links)
            recipient_parts = []
            
            # Firmenname (immer zuerst)
            if motivation_letter.recipient_company and motivation_letter.recipient_company != "Nicht angegeben":
                recipient_parts.append(f"<b>{motivation_letter.recipient_company}</b>")
            
            # Firmenadresse
            if motivation_letter.recipient_company_address and motivation_letter.recipient_company_address != "Nicht angegeben":
                address = motivation_letter.recipient_company_address
                # Ersetze Kommas durch Zeilenumbrüche für bessere Formatierung
                if ", " in address:
                    address_lines = address.split(", ")
                    recipient_parts.extend(address_lines)
                else:
                    recipient_parts.append(address)
            
            # Kontaktperson (falls vorhanden und nicht gleich Firmenname)
            if (motivation_letter.recipient_name and 
                motivation_letter.recipient_name != "Nicht angegeben" and 
                motivation_letter.recipient_name != motivation_letter.recipient_company):
                recipient_parts.append("")  # Leerzeile
                recipient_parts.append(f"z.H. {motivation_letter.recipient_name}")
            
            if recipient_parts:
                recipient_text = "<br/>".join(recipient_parts)
                story.append(Paragraph(recipient_text, self.styles['Recipient']))
            else:
                # Fallback, falls keine Empfängerinformationen vorhanden sind
                story.append(Paragraph("Empfänger", self.styles['Recipient']))
            
            # 3. Datum (rechts)
            date_text = self._format_german_date()
            story.append(Paragraph(date_text, self.styles['Date']))
            
            # 4. Betreff
            subject_text = f"<b>{motivation_letter.subject}</b>"
            story.append(Paragraph(subject_text, self.styles['Subject']))
            
            # 5. Haupttext (in Absätze aufgeteilt) - Anrede ist bereits im Content enthalten
            content_paragraphs = self._format_content_paragraphs(motivation_letter.content)
            for paragraph in content_paragraphs:
                # Füge GitHub-Projekt-Hyperlinks hinzu
                paragraph_with_links = self._add_github_links_to_paragraph(paragraph)
                story.append(Paragraph(paragraph_with_links, self.styles['MainText']))
                story.append(Spacer(1, 6))
            
            # 7. Grußformel
            story.append(Paragraph("Mit freundlichen Grüßen", self.styles['Closing']))
            
            # 8. Signatur
            story.append(Paragraph(motivation_letter.sender_name, self.styles['Signature']))
            
            # PDF generieren
            doc.build(story)
            
            logger.info(f"Template-basiertes PDF erstellt: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Fehler bei Template-PDF-Erstellung: {e}")
            raise
    
    def _format_german_date(self) -> str:
        """Formatiert Datum auf Deutsch"""
        today = datetime.now()
        months = [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ]
        
        # Ort hinzufügen (kann konfiguriert werden)
        location = "Winikon"  # Basierend auf Adresse
        return f"{location}, {today.day}. {months[today.month - 1]} {today.year}"
    
    def _get_german_salutation(self, recipient_name: str) -> str:
        """Erstellt passende deutsche Anrede"""
        if recipient_name and recipient_name != "Nicht angegeben":
            # Versuche Geschlecht zu erkennen (einfache Heuristik)
            if any(title in recipient_name.lower() for title in ["frau", "ms.", "mrs."]):
                return "Sehr geehrte Frau [Name],"
            elif any(title in recipient_name.lower() for title in ["herr", "mr."]):
                return "Sehr geehrter Herr [Name],"
            else:
                return "Sehr geehrte Damen und Herren,"
        else:
            return "Sehr geehrte Damen und Herren,"
    
    def _format_content_paragraphs(self, content: str) -> list:
        """Formatiert Inhalt in deutsche Absätze und entfernt doppelte Anreden"""
        # Inhalt in Absätze aufteilen
        paragraphs = content.split('\n\n')
        
        formatted_paragraphs = []
        for paragraph in paragraphs:
            if paragraph.strip():
                # Deutschen Stil anwenden
                formatted_paragraph = paragraph.strip()
                
                # Entferne doppelte Anreden (falls LLM beide generiert hat)
                if (formatted_paragraph.startswith("Sehr geehrte Damen und Herren") or 
                    formatted_paragraph == "Sehr geehrte Damen und Herren," or
                    formatted_paragraph.startswith("Sehr geehrte Damen und Herren,")):
                    continue
                
                # Entferne Grußformeln aus dem Inhalt, da sie separat hinzugefügt werden
                if (formatted_paragraph.startswith("Mit freundlichen Grüßen") or 
                    formatted_paragraph.startswith("Mit freundlichen Grüssen") or
                    formatted_paragraph.startswith("Freundliche Grüße") or
                    formatted_paragraph.startswith("Freundliche Grüsse") or
                    formatted_paragraph.startswith("Vielen Dank") or
                    formatted_paragraph.startswith("Herzlichen Dank")):
                    continue
                    
                # Entferne auch Namen am Ende, die wie eine Signatur aussehen
                words = formatted_paragraph.split()
                if len(words) <= 3:
                    # Prüfe, ob es sich um eine Signatur handelt
                    if any(word.lower() in ['daniel', 'zurmühle'] for word in words):
                        continue
                        
                formatted_paragraphs.append(formatted_paragraph)
        
        return formatted_paragraphs
    
    def get_template_info(self) -> dict:
        """Gibt Template-Informationen zurück"""
        if self.template_analysis:
            return {
                "template_found": True,
                "pages": self.template_analysis.get("pages", 0),
                "analysis": self.template_analysis
            }
        else:
            return {
                "template_found": False,
                "message": "Kein Template gefunden oder Analyse fehlgeschlagen"
            }
    
    def create_pdf(self, motivation_letter: MotivationLetter, 
                   output_dir: str = "output") -> str:
        """Hauptmethode - verwendet Template falls verfügbar"""
        if self.template_analysis:
            logger.info("Verwende Template-basierte PDF-Erstellung")
            return self.create_pdf_from_template(motivation_letter, output_dir)
        else:
            logger.info("Verwende Standard-PDF-Erstellung")
            return self.create_standard_pdf(motivation_letter, output_dir)
    
    def _add_github_links_to_paragraph(self, paragraph_text):
        """Fügt GitHub-Projekt-Hyperlinks und LinkedIn-Links zu einem Absatz hinzu"""
        # Regex-Pattern für GitHub-Projekt-Erwähnungen
        # Sucht nach GitHub-Projektnamen direkt
        github_project_pattern = r'\b(ZurdLLMWS|AutomaticMotivation|Auto-search-jobs)\b'
        
        # Regex-Pattern für LinkedIn-Erwähnungen
        # Sucht nach: "LinkedIn-Profil" oder "LinkedIn Profil"
        linkedin_pattern = r"(LinkedIn[\s\-]?Profil)"
        
        # Verwende Config für dynamische URL-Generierung
        project_urls = Config.get_github_project_urls()
        linkedin_url = Config.PERSONAL_LINKEDIN
        
        def replace_project_with_link(match):
            project_name = match.group(1)    # "ProjectName"
            
            # GitHub-URL für das Projekt suchen
            github_url = project_urls.get(project_name)
            
            if github_url:
                # Erstelle Hyperlink im ReportLab-Format
                return f'<a href="{github_url}" color="blue">{project_name}</a>'
            else:
                # Kein Link verfügbar, verwende normalen Text
                return project_name
        
        def replace_linkedin_with_link(match):
            linkedin_text = match.group(1)
            
            if linkedin_url:
                # Erstelle LinkedIn-Hyperlink im ReportLab-Format
                return f'<a href="{linkedin_url}" color="blue">{linkedin_text}</a>'
            else:
                # Kein Link verfügbar, verwende normalen Text
                return linkedin_text
        
        # Ersetze alle Projekt-Erwähnungen durch Links
        processed_text = re.sub(github_project_pattern, replace_project_with_link, paragraph_text)
        
        # Ersetze LinkedIn-Erwähnungen durch Links
        processed_text = re.sub(linkedin_pattern, replace_linkedin_with_link, processed_text)
        
        return processed_text
    
    def create_standard_pdf(self, motivation_letter: MotivationLetter, 
                          output_dir: str = "output") -> str:
        """Standard-PDF-Erstellung als Fallback"""
        # Hier würde die ursprüngliche PDF-Erstellung stehen
        return self.create_pdf_from_template(motivation_letter, output_dir)
