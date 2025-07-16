import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
import pdfplumber
import logging
from src.models import MotivationLetter
from config.config import Config

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Klasse zum Generieren von PDF-Motivationsschreiben mit Template-Unterstützung"""
    
    def __init__(self, template_path: str = None):
        self.template_path = template_path or "templates/template.pdf"
        self.page_width, self.page_height = A4
        self.margin = 2 * cm
        self.styles = getSampleStyleSheet()
        self._setup_german_styles()
        
    def _setup_german_styles(self):
        """Richtet deutsche Styles für Motivationsschreiben ein"""
        # Bevorzugte Schriftart: Aptos Display (falls verfügbar), sonst Helvetica
        preferred_font = 'Aptos-Display'
        preferred_font_bold = 'Aptos-Display-Bold'
        fallback_font = 'Helvetica'
        fallback_font_bold = 'Helvetica-Bold'
        
        # Teste ob Aptos Display verfügbar ist, sonst verwende Helvetica
        try:
            from reportlab.pdfbase import pdfmetrics
            # Versuche Aptos Display zu registrieren (falls verfügbar)
            font_name = preferred_font
            font_bold = preferred_font_bold
        except:
            # Fallback zu Helvetica
            font_name = fallback_font
            font_bold = fallback_font_bold
        
        # Verwende Helvetica als sichere Fallback-Option
        font_name = fallback_font
        font_bold = fallback_font_bold
        
        # Absender-Style (oben rechts)
        self.styles.add(ParagraphStyle(
            name='Sender',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_RIGHT,
            spaceAfter=6,
            fontName=font_name
        ))
        
        # Empfänger-Style (links)
        self.styles.add(ParagraphStyle(
            name='Recipient',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=12,
            spaceBefore=24,
            fontName=font_name
        ))
        
        # Datum-Style (rechts)
        self.styles.add(ParagraphStyle(
            name='Date',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_RIGHT,
            spaceAfter=24,
            fontName=font_name
        ))
        
        # Betreff-Style (fett)
        self.styles.add(ParagraphStyle(
            name='Subject',
            parent=self.styles['Normal'],
            fontSize=14,
            alignment=TA_LEFT,
            spaceAfter=18,
            fontName=font_bold
        ))
        
        # Anrede-Style
        self.styles.add(ParagraphStyle(
            name='Salutation',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=12,
            fontName=font_name
        ))
        
        # Haupttext-Style (Blocksatz wie im deutschen Standard)
        self.styles.add(ParagraphStyle(
            name='MainText',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16,
            fontName=font_name
        ))
        
        # Grußformel-Style
        self.styles.add(ParagraphStyle(
            name='Closing',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=36,
            spaceBefore=12,
            fontName=font_name
        ))
        
        # Signatur-Style
        self.styles.add(ParagraphStyle(
            name='Signature',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            fontName=font_name
        ))
    
    def create_pdf(self, motivation_letter: MotivationLetter, output_dir: str = "output") -> str:
        """
        Erstellt ein PDF-Motivationsschreiben im deutschen Standard-Format
        
        Args:
            motivation_letter: MotivationLetter-Objekt
            output_dir: Ausgabeordner
            
        Returns:
            str: Pfad zur erstellten PDF-Datei
        """
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
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )
            
            # Inhalt erstellen
            story = []
            
            # 1. Absender (oben rechts - Ihr Format)
            sender_text = self._format_sender_address(motivation_letter)
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
                # Prüfe auf GitHub-Projekt-Erwähnungen und erstelle Hyperlinks
                formatted_paragraph = self._add_github_links_to_paragraph(paragraph)
                story.append(Paragraph(formatted_paragraph, self.styles['MainText']))
                story.append(Spacer(1, 6))
            
            # 6. Grußformel
            story.append(Paragraph("Mit freundlichen Grüßen", self.styles['Closing']))
            
            # 7. Signatur
            story.append(Paragraph(motivation_letter.sender_name, self.styles['Signature']))
            
            # PDF generieren
            doc.build(story)
            
            logger.info(f"PDF erfolgreich erstellt: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Fehler bei PDF-Erstellung: {e}")
            raise
    
    def _format_sender_address(self, motivation_letter: MotivationLetter) -> str:
        """Formatiert die Absenderadresse im korrekten deutschen Format"""
        # Extrahiere Adressteile
        address_parts = motivation_letter.sender_address.split(', ')
        
        if len(address_parts) >= 2:
            # Format: "Straße Hausnummer, PLZ Ort"
            street = address_parts[0].strip()
            city_part = address_parts[1].strip()
            
            # Versuche PLZ und Ort zu trennen
            city_parts = city_part.split(' ')
            if len(city_parts) >= 2:
                postal_code = city_parts[0]
                city = ' '.join(city_parts[1:])
            else:
                postal_code = ""
                city = city_part
            
            return f"""
            {motivation_letter.sender_name}<br/>
            {street}<br/>
            {postal_code} {city}<br/>
            Tel: {motivation_letter.sender_phone}<br/>
            E-Mail: {motivation_letter.sender_email}
            """
        else:
            # Fallback für unbekanntes Format
            return f"""
            {motivation_letter.sender_name}<br/>
            {motivation_letter.sender_address}<br/>
            Tel: {motivation_letter.sender_phone}<br/>
            E-Mail: {motivation_letter.sender_email}
            """
    
    def _format_german_date(self) -> str:
        """Formatiert Datum auf Deutsch"""
        today = datetime.now()
        months = [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ]
        
        # Ort aus Adresse extrahieren
        location = "Winikon"  # Aus Ihrer Adresse
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
                # Prüfe, ob der Absatz nur aus einem Namen besteht (weniger als 4 Wörter)
                words = formatted_paragraph.split()
                if len(words) <= 3:
                    # Prüfe, ob es sich um eine Signatur handelt
                    # Typische Signaturen: "Daniel Zurmühle", "Ihr Daniel Zurmühle", etc.
                    if any(word.lower() in ['daniel', 'zurmühle'] for word in words):
                        continue
                        
                formatted_paragraphs.append(formatted_paragraph)
        
        return formatted_paragraphs
    
    def analyze_template(self, template_path: str = None) -> dict:
        """
        Analysiert das PDF-Template
        
        Args:
            template_path: Pfad zum Template
            
        Returns:
            dict: Template-Analyse
        """
        if template_path is None:
            template_path = self.template_path
            
        try:
            if not os.path.exists(template_path):
                logger.warning(f"Template nicht gefunden: {template_path}")
                return {"template_found": False, "error": "File not found"}
                
            analysis = {
                "template_found": True,
                "pages": 0,
                "text_content": "",
                "layout": {},
                "file_size": os.path.getsize(template_path)
            }
            
            # Versuche PDF zu öffnen
            try:
                with pdfplumber.open(template_path) as pdf:
                    analysis["pages"] = len(pdf.pages)
                    
                    for page_num, page in enumerate(pdf.pages):
                        # Text extrahieren
                        text = page.extract_text()
                        if text:
                            analysis["text_content"] += text + "\n"
                        
                        # Layout-Informationen
                        analysis["layout"][f"page_{page_num}"] = {
                            "width": page.width,
                            "height": page.height,
                            "bbox": page.bbox
                        }
                        
                        # Nur erste Seite für Analyse
                        if page_num == 0:
                            break
                
                logger.info(f"Template analysiert: {analysis['pages']} Seiten")
                return analysis
                
            except Exception as pdf_error:
                logger.warning(f"Fehler beim Öffnen der PDF: {pdf_error}")
                # Fallback: Template als vorhanden markieren, aber ohne Analyse
                return {
                    "template_found": True,
                    "pages": 1,
                    "text_content": "",
                    "layout": {},
                    "file_size": os.path.getsize(template_path),
                    "error": f"PDF-Analyse fehlgeschlagen: {pdf_error}"
                }
            
        except Exception as e:
            logger.error(f"Fehler bei Template-Analyse: {e}")
            return {"template_found": False, "error": str(e)}
    
    def create_pdf_with_template(self, motivation_letter: MotivationLetter, 
                               template_path: str = None, output_dir: str = "output") -> str:
        """
        Erstellt ein PDF basierend auf einer Vorlage
        
        Args:
            motivation_letter: MotivationLetter-Objekt
            template_path: Pfad zur PDF-Vorlage
            output_dir: Ausgabeordner
            
        Returns:
            str: Pfad zur erstellten PDF-Datei
        """
        try:
            if template_path and os.path.exists(template_path):
                # Hier würde die Vorlage analysiert und verwendet werden
                # Für jetzt verwenden wir die Standard-Erstellung
                logger.info(f"Vorlage gefunden: {template_path}")
                # TODO: Template-Analyse und -Verwendung implementieren
                
            # Fallback auf Standard-PDF-Erstellung
            return self.create_pdf(motivation_letter, output_dir)
            
        except Exception as e:
            logger.error(f"Fehler bei Template-PDF-Erstellung: {e}")
            raise
    
    def analyze_template(self, template_path: str) -> dict:
        """
        Analysiert eine PDF-Vorlage
        
        Args:
            template_path: Pfad zur PDF-Vorlage
            
        Returns:
            dict: Template-Analyse
        """
        try:
            if not os.path.exists(template_path):
                raise FileNotFoundError(f"Vorlage nicht gefunden: {template_path}")
            
            # Hier würde die PDF-Vorlage analysiert werden
            # Für jetzt geben wir eine Dummy-Analyse zurück
            analysis = {
                "pages": 1,
                "format": "A4",
                "fields": [
                    "sender_name",
                    "sender_address", 
                    "recipient_name",
                    "recipient_address",
                    "date",
                    "subject",
                    "content"
                ],
                "template_path": template_path
            }
            
            logger.info(f"Vorlage analysiert: {template_path}")
            return analysis
            
        except Exception as e:
            logger.error(f"Fehler bei Template-Analyse: {e}")
            raise
    
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
