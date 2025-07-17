#!/usr/bin/env python3
"""
Test für RecipientController-Integration
Testet die Integration des RecipientControllers in die Anwendung
"""

import os
import sys
import tempfile
from docx import Document
import pdfplumber

# Füge src-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # Für root-level imports

from src.ai_generator import AIGenerator
from src.pdf_generator import PDFGenerator
from src.docx_generator import DocxGenerator
from src.models import JobDescription
from src.recipient_controller import RecipientController
from config.config import Config

def test_recipient_controller_integration():
    """Testet die Integration des RecipientControllers"""
    print("=== Test: RecipientController Integration ===\n")
    
    # Test 1: Keine Kontaktperson - sollte Firmenname verwenden
    print("Test 1: Keine Kontaktperson")
    job_description_no_contact = JobDescription(
        position='Senior Developer',
        company='Innovative Tech Solutions',
        contact_person='',  # Keine Kontaktperson
        description='Entwicklung moderner Web-Anwendungen',
        requirements='Python, JavaScript, React',
        benefits='Flexible Arbeitszeiten, Homeoffice',
        location='Zürich',
        address='',  # Keine Adresse
        department='IT',
        url='https://example.com/job1',
        working_hours='100%'
    )
    
    ai_generator = AIGenerator()
    
    # Teste Empfänger-Kontrolle
    controller = RecipientController()
    normalized_job = controller.normalize_recipient_info(job_description_no_contact)
    validation = controller.validate_recipient_info(job_description_no_contact)
    
    print(f"Original Kontaktperson: '{job_description_no_contact.contact_person}'")
    print(f"Normalisierte Kontaktperson: '{normalized_job.contact_person}'")
    print(f"Original Adresse: '{job_description_no_contact.address}'")
    print(f"Normalisierte Adresse: '{normalized_job.address}'")
    print(f"Validierung: {validation}")
    
    # Teste Anrede-Generierung
    salutation = ai_generator._generate_salutation(normalized_job)
    print(f"Generierte Anrede: '{salutation}'")
    
    # Test 2: Generische Kontaktperson - sollte Firmenname verwenden
    print(f"\nTest 2: Generische Kontaktperson")
    job_description_generic = JobDescription(
        position='IT Support Specialist',
        company='MegaCorp AG',
        contact_person='HR Team',  # Generische Kontaktperson
        description='IT Support für Endbenutzer',
        requirements='IT Support, Kundenservice',
        benefits='Gute Sozialleistungen',
        location='Basel',
        address='MegaCorp AG, Hauptstrasse 123, 4000 Basel',
        department='IT',
        url='https://example.com/job2',
        working_hours='80%'
    )
    
    normalized_job2 = controller.normalize_recipient_info(job_description_generic)
    validation2 = controller.validate_recipient_info(job_description_generic)
    
    print(f"Original Kontaktperson: '{job_description_generic.contact_person}'")
    print(f"Normalisierte Kontaktperson: '{normalized_job2.contact_person}'")
    print(f"Validierung: {validation2}")
    
    salutation2 = ai_generator._generate_salutation(normalized_job2)
    print(f"Generierte Anrede: '{salutation2}'")
    
    # Test 3: Vollständige Anwendung mit Dokumentgenerierung
    print(f"\nTest 3: Vollständige Anwendung mit Dokumentgenerierung")
    job_description_complete = JobDescription(
        position='Data Analyst',
        company='DataCorp Solutions',
        contact_person='',  # Keine Kontaktperson
        description='Analyse großer Datenmengen',
        requirements='SQL, Python, Statistik',
        benefits='Spannende Projekte',
        location='Bern',
        address='DataCorp Solutions, Bern',  # Unvollständige Adresse
        department='Analytics',
        url='https://example.com/job3',
        working_hours='100%'
    )
    
    # Vollständige Motivationsschreiben-Generierung
    motivation_letter = ai_generator.generate_motivation_letter(job_description_complete)
    
    print(f"Empfänger-Unternehmen: '{motivation_letter.recipient_company}'")
    print(f"Empfänger-Name: '{motivation_letter.recipient_name}'")
    print(f"Empfänger-Adresse: '{motivation_letter.recipient_company_address}'")
    print(f"Betreff: '{motivation_letter.subject}'")
    
    # Zeige erste Zeile des Inhalts (sollte korrekte Anrede enthalten)
    first_line = motivation_letter.content.split('\n')[0]
    print(f"Erste Zeile (Anrede): '{first_line}'")
    
    # Test 4: Dokument-Generierung
    print(f"\nTest 4: Dokument-Generierung")
    
    # PDF erstellen
    pdf_generator = PDFGenerator()
    pdf_path = pdf_generator.create_pdf(motivation_letter)
    print(f"PDF erstellt: {pdf_path}")
    
    # DOCX erstellen
    docx_generator = DocxGenerator()
    docx_path = docx_generator.create_docx(motivation_letter)
    print(f"DOCX erstellt: {docx_path}")
    
    # Prüfe Empfänger-Informationen in PDF
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            pdf_text = first_page.extract_text()
            
            print(f"\nPDF-Inhalt (erste 300 Zeichen):")
            print(pdf_text[:300])
            
            # Suche nach Empfänger-Informationen
            if "DataCorp Solutions" in pdf_text:
                print("✅ Firmenname korrekt im PDF gefunden")
            else:
                print("❌ Firmenname nicht im PDF gefunden")
                
    except Exception as e:
        print(f"Fehler beim Lesen der PDF: {e}")
    
    # Prüfe Empfänger-Informationen in DOCX
    try:
        doc = Document(docx_path)
        docx_text = ""
        for paragraph in doc.paragraphs:
            docx_text += paragraph.text + "\n"
        
        print(f"\nDOCX-Inhalt (erste 300 Zeichen):")
        print(docx_text[:300])
        
        # Suche nach Empfänger-Informationen
        if "DataCorp Solutions" in docx_text:
            print("✅ Firmenname korrekt im DOCX gefunden")
        else:
            print("❌ Firmenname nicht im DOCX gefunden")
            
    except Exception as e:
        print(f"Fehler beim Lesen der DOCX: {e}")
    
    # Cleanup
    try:
        os.remove(pdf_path)
        os.remove(docx_path)
        print(f"\nTest-Dateien bereinigt.")
    except:
        pass
    
    print("\n=== Test abgeschlossen ===")

if __name__ == "__main__":
    test_recipient_controller_integration()
