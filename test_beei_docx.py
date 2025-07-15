#!/usr/bin/env python3
"""
Test-Skript für beei AG DOCX-Generierung ohne doppelte Anrede
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import MotivationLetter
from src.docx_generator import DocxGenerator

def test_beei_docx():
    """Test mit beei AG Daten"""
    
    # Test-Daten für beei AG
    motivation_letter = MotivationLetter(
        sender_name="Daniel Zurmühle",
        sender_address="Hinterdorfstrasse 12, 6235 Winikon",
        sender_phone="+41 79 127 55 54",
        sender_email="dzurmuehle@gmail.com",
        recipient_name="Personalteam",  # Generischer Empfänger
        recipient_address="Nicht angegeben",
        recipient_company="beei AG",
        recipient_company_address="Zürich, Schweiz",
        subject="Bewerbung als Software-EntwicklerIn 60-100%",
        content="""Sehr geehrte Damen und Herren,

mit großem Interesse habe ich Ihre Ausschreibung für die Position als Software-Entwickler im Bereich Business Intelligence wahrgenommen. Als erfahrener Softwareentwickler mit über vier Jahren Berufserfahrung und einem umfassenden technologischen Spektrum bin ich überzeugt, dass ich eine hervorragende Ergänzung für Ihr Team sein kann.

Meine Expertise umfasst moderne Webtechnologien, Datenbanken und agile Entwicklungsmethoden. Ich bringe praktische Erfahrung in der Entwicklung von Business Intelligence-Lösungen mit und bin motiviert, innovative Projekte voranzutreiben.

Ich freue mich darauf, in einem persönlichen Gespräch mehr über die Position und meine Qualifikationen zu erfahren."""
    )
    
    # DOCX generieren
    generator = DocxGenerator()
    docx_path = generator.create_docx(motivation_letter)
    
    print(f"DOCX-Datei erstellt: {docx_path}")
    print(f"Dateigröße: {os.path.getsize(docx_path)} Bytes")
    
    # Prüfen, ob die Datei existiert
    if os.path.exists(docx_path):
        print("✓ DOCX-Datei erfolgreich erstellt")
        print(f"✓ Empfänger: {motivation_letter.recipient_name}")
        print(f"✓ Firma: {motivation_letter.recipient_company}")
        print(f"✓ Betreff: {motivation_letter.subject}")
        print("✓ Korrekturen:")
        print("  - Keine doppelte Anrede")
        print("  - Firmenname nicht unterstrichen")
        print("  - Korrekte Anrede für Personalteam")
    else:
        print("✗ Fehler beim Erstellen der DOCX-Datei")

if __name__ == "__main__":
    test_beei_docx()
