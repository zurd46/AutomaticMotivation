#!/usr/bin/env python3
"""
Test-Skript für DOCX-Generierung
"""

import sys
import os
from datetime import datetime

# Pfad zum Hauptverzeichnis hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import MotivationLetter
from src.docx_generator import DocxGenerator

def test_docx_generation():
    """Testet die DOCX-Generierung mit korrekter Position + Arbeitszeit"""
    
    print("=" * 60)
    print("🧪 DOCX-Generierung Test (mit Arbeitszeit)")
    print("=" * 60)
    
    # Test-Motivationsschreiben mit Position + Arbeitszeit
    motivation_letter = MotivationLetter(
        recipient_company="beei AG",
        recipient_company_address="Zürich, Schweiz",
        recipient_name="Personalteam",
        recipient_address="Zürich, Schweiz",
        subject="Bewerbung als Software-EntwicklerIn 60-100%",  # Mit Arbeitszeit!
        content="""mit großem Interesse habe ich Ihre Stellenausschreibung für die Position als Software-EntwicklerIn 60-100% gelesen. Als erfahrener Entwickler mit mehrjähriger Berufserfahrung bin ich davon überzeugt, dass ich eine wertvolle Ergänzung für Ihr Team sein kann.

Meine Expertise in der Softwareentwicklung und meine Flexibilität bezüglich der Arbeitszeit (60-100%) passen perfekt zu den Anforderungen Ihrer Stelle. Besonders reizt mich die Möglichkeit, innovative Lösungen zu entwickeln.

Gerne würde ich mich persönlich bei Ihnen vorstellen und dabei erläutern, wie ich mit meiner Erfahrung zur Weiterentwicklung der beei AG beitragen kann.""",
        sender_name="Max Mustermann",
        sender_address="Musterstraße 123, 12345 Musterstadt",
        sender_phone="+49 123 456789",
        sender_email="max.mustermann@example.com"
    )
    
    try:
        # DOCX-Generator erstellen
        docx_generator = DocxGenerator()
        
        # DOCX erstellen
        docx_path = docx_generator.create_docx(motivation_letter)
        
        print(f"✅ DOCX erfolgreich erstellt: {docx_path}")
        print(f"📋 Subject: {motivation_letter.subject}")
        
        # Datei-Informationen anzeigen
        if os.path.exists(docx_path):
            file_size = os.path.getsize(docx_path)
            print(f"📊 Dateigröße: {file_size:,} Bytes")
            print(f"📅 Erstellt: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
            
            # Pfad für Benutzer anzeigen
            abs_path = os.path.abspath(docx_path)
            print(f"🔗 Vollständiger Pfad: {abs_path}")
        else:
            print("❌ Datei wurde nicht erstellt")
            
    except Exception as e:
        print(f"❌ Fehler bei der DOCX-Erstellung: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n✅ Test abgeschlossen!")

if __name__ == "__main__":
    test_docx_generation()
