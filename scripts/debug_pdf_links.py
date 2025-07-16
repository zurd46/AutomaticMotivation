#!/usr/bin/env python3
"""
Test-Skript für GitHub-Links in PDF
"""

from src.pdf_generator import PDFGenerator
from src.models import MotivationLetter

# Test-Motivationsschreiben mit GitHub-Projekten
test_letter = MotivationLetter(
    sender_name='Daniel Zurmühle',
    sender_address='Hinterdorfstrasse 12, 6235 Winikon',
    sender_phone='+41 79 127 55 54',
    sender_email='dzurmuehle@gmail.com',
    recipient_company='GitHub Test Company PDF',
    recipient_company_address='Test Address',
    recipient_address='Test Address',
    recipient_name='Test Person',
    subject='Bewerbung als Softwareentwickler',
    content='Sehr geehrte Damen und Herren,\n\nIch habe bereits an mehreren Projekten gearbeitet, darunter AutomaticMotivation und ZurdLLMWS. Diese Projekte zeigen meine Fähigkeiten in der Softwareentwicklung.\n\nMein LinkedIn-Profil finden Sie unter meinem Namen.\n\nMit freundlichen Grüßen'
)

print("Generiere PDF mit GitHub-Links...")
generator = PDFGenerator()
filepath = generator.create_pdf(test_letter)
print(f"PDF erstellt: {filepath}")

# Test der GitHub-Link-Verarbeitung
print("\nTest der GitHub-Link-Verarbeitung:")
paragraph_text = "Ich habe bereits an mehreren Projekten gearbeitet, darunter AutomaticMotivation und ZurdLLMWS. Diese Projekte zeigen meine Fähigkeiten in der Softwareentwicklung."
processed_text = generator._add_github_links_to_paragraph(paragraph_text)
print(f"Original: {paragraph_text}")
print(f"Verarbeitet: {processed_text}")

# LinkedIn-Test
linkedin_text = "Mein LinkedIn-Profil finden Sie unter meinem Namen."
processed_linkedin = generator._add_github_links_to_paragraph(linkedin_text)
print(f"LinkedIn Original: {linkedin_text}")
print(f"LinkedIn Verarbeitet: {processed_linkedin}")
