#!/usr/bin/env python3
"""
Test der Absatz-Struktur in generierten Motivationsschreiben
"""

import os
import sys
import re

# Pfad zum src-Verzeichnis hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import JobDescription
from src.ai_generator import AIGenerator

def test_paragraph_structure():
    """Test der Absatz-Struktur"""
    print("=== TEST: Absatz-Struktur ===")
    
    # IT-Support-Stellenbeschreibung
    job_description = JobDescription(
        url="https://example.com/it-support",
        position="ICT Supporter",
        company="Luzerner Kantonsspital",
        location="Luzern",
        department="IT",
        description="ICT Support für Anwender und Systeme",
        requirements="Support-Erfahrung, Problemlösung, Kommunikation",
        benefits="Vollzeit, dynamisches Team",
        contact_person="Michael Enz",
        address="Spitalstrasse 1, 6000 Luzern"
    )
    
    # Teste AI-Generator
    try:
        ai_generator = AIGenerator()
        motivation_letter = ai_generator.generate_motivation_letter(job_description)
        
        print(f"✅ Generierung erfolgreich")
        print(f"Unternehmen: {motivation_letter.recipient_company}")
        print(f"Position: {job_description.position}")
        print(f"Betreff: {motivation_letter.subject}")
        print("\n--- VOLLSTÄNDIGER CONTENT ---")
        print(motivation_letter.content)
        print("--- END CONTENT ---\n")
        
        # Prüfe Absatz-Struktur
        paragraphs = motivation_letter.content.split('\n\n')
        print(f"📊 Anzahl Absätze: {len(paragraphs)}")
        
        for i, paragraph in enumerate(paragraphs, 1):
            print(f"Absatz {i}: {paragraph[:80]}...")
        
        # Prüfe auf Projekt-Erwähnungen
        if re.search(r'projekt', motivation_letter.content.lower()):
            print("❌ FEHLER: Projekt-Erwähnungen gefunden!")
            return False
        else:
            print("✅ SUCCESS: Keine Projekt-Erwähnungen gefunden")
            
        # Prüfe auf korrekte Absätze
        if len(paragraphs) >= 3:
            print("✅ SUCCESS: Absätze korrekt strukturiert")
            return True
        else:
            print("⚠️  WARNING: Weniger als 3 Absätze gefunden")
            return False
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    success = test_paragraph_structure()
    sys.exit(0 if success else 1)
