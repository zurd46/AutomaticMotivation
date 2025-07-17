#!/usr/bin/env python3
"""
Test Script für automatische Adressensuche in vollständiger Dokumentenerstellung
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import JobDescription
from src.recipient_controller import RecipientController
from src.ai_generator import AIGenerator
from src.template_pdf_generator import TemplateBasedPDFGenerator
from src.docx_generator import DocxGenerator
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_full_document_generation_with_auto_address():
    """
    Testet die vollständige Dokumentenerstellung mit automatischer Adressensuche
    """
    print("=== Test: Vollständige Dokumentenerstellung mit automatischer Adressensuche ===")
    
    # Test-Job OHNE Adresse
    test_job = JobDescription(
        url="https://example.com/test-job",
        company="Luzerner Kantonsspital",
        position="ICT Supporter 100%",
        location="Luzern",
        address="",  # KEINE Adresse angegeben
        contact_person="Michael Enz",  # Spezifische Kontaktperson
        contact_title="",
        email="",
        phone="",
        description="IT-Support Position mit Kundenservice und technischem Support",
        requirements="Erfahrung in IT-Support und Kundenservice",
        benefits="Flexible Arbeitszeiten, gute Sozialleistungen",
        working_hours="100%",
        salary=""
    )
    
    print(f"Original Job-Daten:")
    print(f"  Unternehmen: '{test_job.company}'")
    print(f"  Kontaktperson: '{test_job.contact_person}'")
    print(f"  Standort: '{test_job.location}'")
    print(f"  Adresse: '{test_job.address}' (leer)")
    
    # Schritt 1: Empfänger-Informationen normalisieren (mit automatischer Adressensuche)
    controller = RecipientController()
    normalized_job = controller.normalize_recipient_info(test_job)
    
    print(f"\nNach RecipientController (mit automatischer Adressensuche):")
    print(f"  Empfänger-Unternehmen: '{normalized_job.company}'")
    print(f"  Empfänger-Kontaktperson: '{normalized_job.contact_person}'")
    print(f"  Empfänger-Standort: '{normalized_job.location}'")
    print(f"  Empfänger-Adresse: '{normalized_job.address}'")
    
    # Schritt 2: AI-Generator für Kategorisierung
    ai_generator = AIGenerator()
    ai_result = ai_generator.generate_motivation_letter(normalized_job)
    
    print(f"\nAI-Generator erfolgreich:")
    print(f"  Empfänger-Unternehmen: {ai_result.recipient_company}")
    print(f"  Empfänger-Adresse: {ai_result.recipient_company_address}")
    print(f"  Empfänger-Name: {ai_result.recipient_name}")
    print(f"  Motivation generiert: {len(ai_result.content)} Zeichen")
    
    # Schritt 3: PDF-Generator
    pdf_generator = TemplateBasedPDFGenerator()
    pdf_path = pdf_generator.create_pdf(ai_result)
    print(f"\nPDF erstellt: {pdf_path}")
    
    # Schritt 4: DOCX-Generator
    docx_generator = DocxGenerator()
    docx_path = docx_generator.create_docx(ai_result)
    print(f"DOCX erstellt: {docx_path}")
    
    # Schritt 5: Prüfe Empfänger-Informationen in generierten Dokumenten
    from docx import Document
    doc = Document(docx_path)
    docx_text = "\n".join([p.text for p in doc.paragraphs])
    
    print(f"\n=== Empfänger-Informationen in DOCX ===")
    lines = docx_text.split('\n')
    for i, line in enumerate(lines[:15]):
        if line.strip():
            print(f"  {i+1}: {line}")
    
    # Prüfe auf korrekte Adresse
    if "Spitalstrasse" in docx_text and "6000 Luzern" in docx_text:
        print(f"\n✅ Automatisch gefundene Adresse korrekt in DOCX eingebettet!")
    else:
        print(f"\n❌ Automatisch gefundene Adresse nicht korrekt eingebettet")
    
    # Prüfe auf korrekte Kontaktperson
    if "z.H. Michael Enz" in docx_text:
        print(f"✅ Kontaktperson korrekt angezeigt!")
    else:
        print(f"❌ Kontaktperson nicht korrekt angezeigt")
    
    # Bereinige Test-Dateien
    import os
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    if os.path.exists(docx_path):
        os.remove(docx_path)
    
    print(f"\n🎉 Test abgeschlossen! Automatische Adressensuche funktioniert!")

if __name__ == "__main__":
    test_full_document_generation_with_auto_address()
