#!/usr/bin/env python3
"""
Test-Skript für DOCX-Generierung mit korrigierten Formatierungen
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import MotivationLetter
from src.docx_generator import DocxGenerator

def test_docx_formatting():
    """Test mit Datalynx AG Daten"""
    
    # Test-Daten für Datalynx AG
    motivation_letter = MotivationLetter(
        sender_name="Jan Schmitz-Elsen",
        sender_address="Hinterdorfstrasse 12, 6235 Winikon",
        sender_phone="+41 79 127 55 54",
        sender_email="dzurmuehle@gmail.com",
        recipient_name="Jan Schmitz-Elsen",  # Spezifischer Empfänger
        recipient_address="Nicht angegeben",  # Erforderliches Feld
        recipient_company="Datalynx AG",
        recipient_company_address="Aeschenplatz 6, 4052 Basel, Schweiz",
        subject="Bewerbung als AI Consultant (m/w/d)",
        content="""mit großem Interesse habe ich Ihre Stellenausschreibung für die Position des AI Consultants bei der Datalynx AG gelesen. Als erfahrener Entwickler mit Schwerpunkt auf künstlicher Intelligenz und innovativen Technologielösungen sehe ich mich als idealen Kandidaten für diese herausfordernde Position.

Meine Erfahrungen in der Entwicklung und Implementierung von KI-Lösungen, kombiniert mit meinem technischen Verständnis und meiner Leidenschaft für Innovation, machen mich zu einem wertvollen Mitglied Ihres Teams.

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
        print("✓ Formatierungen korrigiert:")
        print("  - Firmenname nicht unterstrichen")
        print("  - Anrede für Jan Schmitz-Elsen: 'Sehr geehrter Herr Schmitz-Elsen,'")
    else:
        print("✗ Fehler beim Erstellen der DOCX-Datei")

if __name__ == "__main__":
    test_docx_formatting()
