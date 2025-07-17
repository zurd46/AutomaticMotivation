#!/usr/bin/env python3
"""
Test-Script für GitHub-Projekt-Hyperlinks
"""

from src.docx_generator import DocxGenerator
from src.pdf_generator import PDFGenerator
from src.models import MotivationLetter
from datetime import datetime

def test_github_links():
    """Testet die GitHub-Projekt-Hyperlink-Funktionalität"""
    
    # Test-Motivationsschreiben erstellen
    test_motivation = MotivationLetter(
        recipient_company="Test AG",
        recipient_company_address="Teststraße 1, 12345 Test, Deutschland",
        recipient_name="Herr Test",
        recipient_address="Teststraße 1, 12345 Test, Deutschland",
        subject="Bewerbung als Test-Position",
        content="""
        Sehr geehrter Herr Test,

        in meinem Projekt 'AutomaticMotivation' habe ich eine innovative KI-basierte Lösung entwickelt. 
        Zusätzlich konnte ich mit dem Projekt 'ZurdLLMWS' meine Expertise in der Webentwicklung unter Beweis stellen.
        
        Mein drittes Projekt 'Auto-search-jobs' zeigt meine Fähigkeiten in der Automatisierung von Bewerbungsprozessen.
        
        Diese Erfahrungen qualifizieren mich perfekt für die ausgeschriebene Position.
        """,
        sender_name="Daniel Zurmühle",
        sender_address="Hinterdorfstrasse 12, 6235 Winikon",
        sender_phone="+41 79 127 55 54",
        sender_email="dzurmuehle@gmail.com",
        date=datetime.now()
    )
    
    # DOCX-Generator testen
    print("📄 Teste DOCX-Generator mit GitHub-Links...")
    docx_generator = DocxGenerator()
    docx_file = docx_generator.create_docx(test_motivation)
    print(f"✅ DOCX erstellt: {docx_file}")
    
    # PDF-Generator testen
    print("\n📄 Teste PDF-Generator mit GitHub-Links...")
    pdf_generator = PDFGenerator()
    pdf_file = pdf_generator.create_pdf(test_motivation)
    print(f"✅ PDF erstellt: {pdf_file}")
    
    print("\n🎉 Test abgeschlossen! Überprüfen Sie die generierten Dateien auf funktionierende GitHub-Links.")

if __name__ == "__main__":
    test_github_links()
