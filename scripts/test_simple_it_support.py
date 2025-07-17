#!/usr/bin/env python3
"""
Einfacher Test für IT-Support ohne GitHub-Projekte
"""

import os
import sys
import re

# Pfad zum src-Verzeichnis hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import JobDescription
from src.ai_generator import AIGenerator

def test_it_support_simple():
    """Einfacher Test für IT-Support-Stelle"""
    print("=== EINFACHER TEST: IT-Support ===")
    
    # IT-Support-Stellenbeschreibung
    job_description = JobDescription(
        url="https://example.com/it-support",
        position="IT-Support Mitarbeiter",
        company="TestFirma GmbH",
        location="Bern",
        department="IT",
        description="IT-Support für Anwender und Systeme",
        requirements="Support-Erfahrung, Problemlösung, Kommunikation",
        benefits="Flexible Arbeitszeiten",
        contact_person="Hr. Test",
        address="Teststrasse 1, 3000 Bern"
    )
    
    # Teste AI-Generator
    try:
        ai_generator = AIGenerator()
        motivation_letter = ai_generator.generate_motivation_letter(job_description)
        
        print(f"✅ Generierung erfolgreich")
        print(f"Content: {motivation_letter.content[:200]}...")
        
        # Prüfe auf Projekt-Erwähnungen
        if re.search(r'projekt', motivation_letter.content.lower()):
            print("❌ FEHLER: Projekt-Erwähnungen gefunden!")
            return False
        else:
            print("✅ SUCCESS: Keine Projekt-Erwähnungen gefunden")
            return True
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    success = test_it_support_simple()
    sys.exit(0 if success else 1)
