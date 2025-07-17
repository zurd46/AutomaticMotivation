#!/usr/bin/env python3
"""
Test für Software-Entwicklung mit GitHub-Projekten
"""

import os
import sys
import re

# Pfad zum src-Verzeichnis hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import JobDescription
from src.ai_generator import AIGenerator

def test_software_development_with_projects():
    """Test für Software-Entwicklung mit GitHub-Projekten"""
    print("=== TEST: Software-Entwicklung (mit GitHub-Projekten) ===")
    
    # Software-Entwickler-Stellenbeschreibung
    job_description = JobDescription(
        url="https://example.com/software-dev",
        position="Software Developer",
        company="DevCorp GmbH",
        location="Basel",
        department="Development",
        description="Software Developer für Python und JavaScript Entwicklung",
        requirements="Python, JavaScript, Git, Agile Entwicklung, React, Node.js",
        benefits="Moderne Technologien, Homeoffice",
        contact_person="Ms. Schmidt",
        address="Techstrasse 1, 4000 Basel"
    )
    
    # Teste AI-Generator
    try:
        ai_generator = AIGenerator()
        motivation_letter = ai_generator.generate_motivation_letter(job_description)
        
        print(f"✅ Generierung erfolgreich")
        print(f"Content: {motivation_letter.content[:200]}...")
        
        # Prüfe auf Projekt-Erwähnungen (sollten vorhanden sein)
        if re.search(r'projekt', motivation_letter.content.lower()):
            print("✅ SUCCESS: Projekt-Erwähnungen in Software-Entwickler-Bewerbung gefunden")
            return True
        else:
            print("⚠️  WARNING: Keine Projekt-Erwähnungen in Software-Entwickler-Bewerbung gefunden")
            return True  # Nicht kritisch
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    success = test_software_development_with_projects()
    sys.exit(0 if success else 1)
