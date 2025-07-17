#!/usr/bin/env python3
"""
Test für die spezifische Luzerner Kantonsspital Stelle
"""

import os
import sys
import tempfile
from docx import Document
import pdfplumber

# Füge src-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ai_generator import AIGenerator
from pdf_generator import PDFGenerator
from docx_generator import DocxGenerator
from models import JobDescription
from config.config import Config

def test_luks_ict_support():
    """Testet die spezifische ICT Support Stelle"""
    print("=== Test: ICT Support Stelle Luzerner Kantonsspital ===\n")
    
    # Job-Daten basierend auf der tatsächlichen Stelle
    job_description = JobDescription(
        position='ICT Supporterin/ICT Supporter 100%',
        company='Luzerner Kantonsspital',
        contact_person='Jan Enz',
        description='ICT Support Position am Luzerner Kantonsspital mit Fokus auf Benutzerunterstützung und First-Level-Support',
        requirements='IT-Support Kenntnisse, Kundenservice, Troubleshooting, Servicedesk-Erfahrung',
        benefits='Attraktive Anstellungskonditionen, Weiterbildungsmöglichkeiten',
        location='Luzern',
        address='Luzerner Kantonsspital, Spitalstrasse 1, 6000 Luzern',
        department='IT',
        url='https://www.luks.ch/karriere/stellenangebote/detail/ict-supporterin-ict-supporter-100-108',
        working_hours='100%'
    )
    
    print(f"Position: {job_description.position}")
    print(f"Unternehmen: {job_description.company}")
    print(f"Kontaktperson: {job_description.contact_person}")
    
    # AI-Generator testen
    ai_generator = AIGenerator()
    expected_salutation = ai_generator._generate_salutation(job_description)
    print(f"Erwartete Anrede: '{expected_salutation}'")
    
    # Motivationsschreiben generieren
    motivation_letter = ai_generator.generate_motivation_letter(job_description)
    
    # Zeige die ersten paar Zeilen des Inhalts
    content_lines = motivation_letter.content.split('\n')
    print(f"\nInhalt (erste 5 Zeilen):")
    for i, line in enumerate(content_lines[:5]):
        print(f"  {i+1}: '{line}'")
    
    # PDF erstellen
    pdf_generator = PDFGenerator()
    pdf_path = pdf_generator.create_pdf(motivation_letter)
    print(f"\nPDF erstellt: {pdf_path}")
    
    # DOCX erstellen
    docx_generator = DocxGenerator()
    docx_path = docx_generator.create_docx(motivation_letter)
    print(f"DOCX erstellt: {docx_path}")
    
    # Anrede aus PDF extrahieren
    pdf_salutation = None
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            pdf_text = first_page.extract_text()
            
            # Suche nach Anrede-Mustern
            lines = pdf_text.split('\n')
            for line in lines:
                if 'Sehr geehrte' in line or 'Sehr geehrter' in line:
                    pdf_salutation = line.strip()
                    break
    except Exception as e:
        print(f"Fehler beim Lesen der PDF: {e}")
    
    # Anrede aus DOCX extrahieren
    docx_salutation = None
    try:
        doc = Document(docx_path)
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if 'Sehr geehrte' in text or 'Sehr geehrter' in text:
                docx_salutation = text
                break
    except Exception as e:
        print(f"Fehler beim Lesen der DOCX: {e}")
    
    # Ergebnisse vergleichen
    print(f"\n=== Anrede-Vergleich ===")
    print(f"AI-Generator: '{expected_salutation}'")
    print(f"PDF:          '{pdf_salutation}'")
    print(f"DOCX:         '{docx_salutation}'")
    
    # Teste ob alle Anreden gleich sind
    success = (pdf_salutation == expected_salutation and 
              docx_salutation == expected_salutation and
              pdf_salutation == docx_salutation)
    
    if success:
        print("✅ ERFOLG: Alle Anreden sind korrekt synchronisiert!")
    else:
        print("❌ FEHLER: Anreden sind nicht synchronisiert!")
    
    # Spezifische Validierung für Jan Enz
    if expected_salutation == "Sehr geehrter Herr Enz,":
        print("✅ ERFOLG: Kontaktperson 'Jan Enz' wurde korrekt als 'Sehr geehrter Herr Enz,' erkannt!")
    else:
        print(f"❌ FEHLER: Kontaktperson 'Jan Enz' sollte 'Sehr geehrter Herr Enz,' ergeben, aber ist '{expected_salutation}'")
        success = False
    
    # Prüfe, ob der Inhalt IT-Support-spezifisch ist (keine GitHub-Projekte erwähnt)
    if "GitHub" not in motivation_letter.content and "Projekt" not in motivation_letter.content:
        print("✅ ERFOLG: Inhalt ist IT-Support-spezifisch (keine GitHub-Projekte erwähnt)")
    else:
        print("❌ WARNUNG: Inhalt könnte GitHub-Projekte enthalten (nicht ideal für IT-Support)")
    
    print(f"\n=== Betreff ===")
    print(f"'{motivation_letter.subject}'")
    
    # Cleanup
    try:
        os.remove(pdf_path)
        os.remove(docx_path)
        print(f"\nTest-Dateien bereinigt.")
    except:
        pass
    
    return success

if __name__ == "__main__":
    success = test_luks_ict_support()
    sys.exit(0 if success else 1)
