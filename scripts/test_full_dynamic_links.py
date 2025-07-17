#!/usr/bin/env python3
"""
Test der vollständigen GitHub-Link-Funktionalität mit dynamischen Projekten
"""

from src.docx_generator import DocxGenerator
from src.pdf_generator import PDFGenerator
from src.models import MotivationLetter

def test_full_functionality():
    # Test-Motivationsschreiben mit verschiedenen GitHub-Projekten
    test_letter = MotivationLetter(
        sender_name='Daniel Zurmühle',
        sender_address='Hinterdorfstrasse 12, 6235 Winikon',
        sender_phone='+41 79 127 55 54',
        sender_email='dzurmuehle@gmail.com',
        recipient_company='GitHub Test Company Final',
        recipient_company_address='Test Address',
        recipient_address='Test Address',
        recipient_name='Test Person',
        subject='Bewerbung als Softwareentwickler',
        content='Sehr geehrte Damen und Herren,\n\nIch habe bereits an mehreren Projekten gearbeitet, darunter AutomaticMotivation, ZurdLLMWS und ZurdSynthDataGen. Darüber hinaus habe ich auch python-ftp-data-uploader und Auto-search-jobs-to-Email entwickelt.\n\nMein LinkedIn-Profil finden Sie unter meinem Namen.\n\nMit freundlichen Grüßen'
    )
    
    print("Teste DOCX-Generierung mit dynamischen GitHub-Links...")
    docx_generator = DocxGenerator()
    docx_filepath = docx_generator.create_docx(test_letter)
    print(f"DOCX erstellt: {docx_filepath}")
    
    print("\nTeste PDF-Generierung mit dynamischen GitHub-Links...")
    pdf_generator = PDFGenerator()
    pdf_filepath = pdf_generator.create_pdf(test_letter)
    print(f"PDF erstellt: {pdf_filepath}")
    
    # Teste die Link-Verarbeitung
    print("\nTeste DOCX-Link-Verarbeitung...")
    test_text = "Ich habe an AutomaticMotivation, ZurdLLMWS und python-ftp-data-uploader gearbeitet."
    
    # Simuliere _add_text_with_github_links
    from config.config import Config
    import re
    
    project_urls = Config.get_github_project_urls()
    escaped_projects = [re.escape(project) for project in project_urls.keys()]
    github_project_pattern = f"({'|'.join(escaped_projects)})"
    
    matches = re.findall(github_project_pattern, test_text)
    print(f"Gefundene Projekte im Text: {matches}")
    
    for match in matches:
        url = project_urls.get(match)
        print(f"  {match} -> {url}")
    
    print("\nTeste PDF-Link-Verarbeitung...")
    processed_text = pdf_generator._add_github_links_to_paragraph(test_text)
    print(f"Original: {test_text}")
    print(f"Verarbeitet: {processed_text}")

if __name__ == "__main__":
    test_full_functionality()
