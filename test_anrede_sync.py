#!/usr/bin/env python3
"""
Test für Anrede-Synchronisation zwischen PDF und DOCX
Stellt sicher, dass beide Generatoren die gleiche Anrede verwenden
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

def test_anrede_synchronisation():
    """Testet, ob PDF und DOCX die gleiche Anrede verwenden"""
    print("=== Test: Anrede-Synchronisation zwischen PDF und DOCX ===\n")
    
    # Test-Job-Daten mit bekannter Kontaktperson
    job_description = JobDescription(
        position='ICT Supporterin/ICT Supporter 100%',
        company='Luzerner Kantonsspital',
        contact_person='Jan Enz',
        description='IT-Support Position am Luzerner Kantonsspital',
        requirements='IT-Support Kenntnisse, Kundenservice, Troubleshooting',
        benefits='Attraktive Anstellungskonditionen',
        location='Luzern',
        address='Luzerner Kantonsspital, Spitalstrasse 1, 6000 Luzern',
        department='IT',
        url='https://www.luks.ch/karriere/stellenangebote/detail/ict-supporterin-ict-supporter-100-108',
        working_hours='100%'
    )
    
    print(f"Kontaktperson: {job_description.contact_person}")
    
    # AI-Generator testen
    ai_generator = AIGenerator()
    expected_salutation = ai_generator._generate_salutation(job_description)
    print(f"Erwartete Anrede vom AI-Generator: '{expected_salutation}'")
    
    # Motivationsschreiben generieren
    motivation_letter = ai_generator.generate_motivation_letter(job_description)
    print(f"Generiertes Motivationsschreiben (erste 100 Zeichen): '{motivation_letter.content[:100]}...'")
    
    # PDF erstellen
    pdf_generator = PDFGenerator()
    pdf_path = pdf_generator.create_pdf(motivation_letter)
    print(f"PDF erstellt: {pdf_path}")
    
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
    print(f"\n=== Vergleich der Anreden ===")
    print(f"AI-Generator Anrede: '{expected_salutation}'")
    print(f"PDF Anrede:          '{pdf_salutation}'")
    print(f"DOCX Anrede:         '{docx_salutation}'")
    
    # Teste ob alle Anreden gleich sind
    success = True
    if pdf_salutation != expected_salutation:
        print(f"❌ FEHLER: PDF-Anrede stimmt nicht mit AI-Generator überein!")
        success = False
    
    if docx_salutation != expected_salutation:
        print(f"❌ FEHLER: DOCX-Anrede stimmt nicht mit AI-Generator überein!")
        success = False
    
    if pdf_salutation != docx_salutation:
        print(f"❌ FEHLER: PDF- und DOCX-Anrede sind unterschiedlich!")
        success = False
    
    if success:
        print("✅ ERFOLG: Alle Anreden sind synchron!")
    
    # Cleanup
    try:
        os.remove(pdf_path)
        os.remove(docx_path)
        print(f"\nTest-Dateien bereinigt.")
    except:
        pass
    
    return success

if __name__ == "__main__":
    success = test_anrede_synchronisation()
    sys.exit(0 if success else 1)
