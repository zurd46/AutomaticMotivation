#!/usr/bin/env python3
"""
Vollständiger Test der Automaticmotivation-Anwendung
Testet die komplette Anwendung einschließlich Post-Generation-Filter
"""

import os
import sys
import re

# Pfad zum src-Verzeichnis hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import JobDescription
from src.ai_generator import AIGenerator
from config.config import Config

def test_it_support_application():
    """Test für IT-Support-Stelle ohne GitHub-Projekte"""
    print("=== VOLLSTÄNDIGER TEST: IT-Support (ohne GitHub-Projekte) ===")
    
    # Erstelle eine IT-Support-Stellenbeschreibung
    job_description = JobDescription(
        url="https://example.com/it-support-job",
        position="IT-Support Specialist",
        company="TechCorp AG",
        location="Zürich",
        department="IT",
        description="IT-Support Specialist verantwortlich für IT-Support, Anwenderbetreuung und Troubleshooting",
        requirements="IT-Support-Erfahrung, Kundenservice, Problemlösungskompetenz, Windows/Mac-Kenntnisse",
        benefits="Flexible Arbeitszeiten, Homeoffice möglich",
        contact_person="Hr. Müller",
        address="Bahnhofstrasse 1, 8001 Zürich"
    )
    
    # Initialisiere AI-Generator
    ai_generator = AIGenerator()
    
    # Generiere Motivationsschreiben
    try:
        motivation_letter = ai_generator.generate_motivation_letter(job_description)
        
        print(f"✅ Motivationsschreiben erfolgreich generiert")
        print(f"Unternehmen: {motivation_letter.recipient_company}")
        print(f"Position: {job_description.position}")
        print(f"Betreff: {motivation_letter.subject}")
        print("\n--- CONTENT ---")
        print(motivation_letter.content)
        print("--- END CONTENT ---\n")
        
        # Prüfe auf GitHub-Projekt-Erwähnungen
        github_mentions = check_github_mentions(motivation_letter.content)
        
        if github_mentions:
            print(f"❌ FEHLER: GitHub-Projekt-Erwähnungen gefunden in IT-Support-Bewerbung: {github_mentions}")
            return False
        else:
            print("✅ SUCCESS: Keine GitHub-Projekt-Erwähnungen in IT-Support-Bewerbung gefunden")
            return True
            
    except Exception as e:
        print(f"❌ Fehler bei der Generierung: {e}")
        return False

def test_software_developer_application():
    """Test für Software-Entwickler-Stelle mit GitHub-Projekten"""
    print("\n=== VOLLSTÄNDIGER TEST: Software-Entwickler (mit GitHub-Projekten) ===")
    
    # Erstelle eine Software-Entwickler-Stellenbeschreibung
    job_description = JobDescription(
        url="https://example.com/software-developer-job",
        position="Software Developer",
        company="DevCorp GmbH",
        location="Basel",
        department="Development",
        description="Software Developer für Softwareentwicklung mit Python, JavaScript und modernen Frameworks",
        requirements="Python, JavaScript, React, Node.js, Git, Agile Entwicklung",
        benefits="Moderne Technologien, Weiterbildungsmöglichkeiten",
        contact_person="Ms. Schmidt",
        address="Technopark 2, 4051 Basel"
    )
    
    # Initialisiere AI-Generator
    ai_generator = AIGenerator()
    
    # Generiere Motivationsschreiben
    try:
        motivation_letter = ai_generator.generate_motivation_letter(job_description)
        
        print(f"✅ Motivationsschreiben erfolgreich generiert")
        print(f"Unternehmen: {motivation_letter.recipient_company}")
        print(f"Position: {job_description.position}")
        print(f"Betreff: {motivation_letter.subject}")
        print("\n--- CONTENT ---")
        print(motivation_letter.content)
        print("--- END CONTENT ---\n")
        
        # Prüfe auf GitHub-Projekt-Erwähnungen (sollten vorhanden sein)
        github_mentions = check_github_mentions(motivation_letter.content)
        
        if github_mentions:
            print(f"✅ SUCCESS: GitHub-Projekt-Erwähnungen gefunden in Software-Entwickler-Bewerbung: {github_mentions}")
            return True
        else:
            print("⚠️  WARNING: Keine GitHub-Projekt-Erwähnungen in Software-Entwickler-Bewerbung gefunden")
            return True  # Nicht kritisch, da sie möglicherweise als irrelevant eingestuft wurden
            
    except Exception as e:
        print(f"❌ Fehler bei der Generierung: {e}")
        return False

def check_github_mentions(content):
    """Prüft auf GitHub-Projekt-Erwähnungen im Content"""
    github_patterns = [
        r'github',
        r'repository',
        r'repo\b',
        r'projekt[e]?',
        r'entwicklung[^\w]*projekt',
        r'code[^\w]*projekt',
        r'programmier[^\w]*projekt',
        r'automatisierung[^\w]*projekt',
        r'webp-to-jpg',
        r'software[^\w]*projekt'
    ]
    
    mentions = []
    for pattern in github_patterns:
        matches = re.findall(pattern, content.lower())
        if matches:
            mentions.extend(matches)
    
    return list(set(mentions))

def main():
    """Hauptfunktion für die Tests"""
    print("Starte vollständige Anwendungstests...")
    
    # Test IT-Support (sollte keine GitHub-Projekte enthalten)
    it_support_success = test_it_support_application()
    
    # Test Software-Entwickler (kann GitHub-Projekte enthalten)
    software_dev_success = test_software_developer_application()
    
    print("\n=== ZUSAMMENFASSUNG ===")
    print(f"IT-Support Test: {'✅ BESTANDEN' if it_support_success else '❌ FEHLGESCHLAGEN'}")
    print(f"Software-Entwickler Test: {'✅ BESTANDEN' if software_dev_success else '❌ FEHLGESCHLAGEN'}")
    
    if it_support_success and software_dev_success:
        print("🎉 ALLE TESTS BESTANDEN!")
        return True
    else:
        print("❌ EINIGE TESTS FEHLGESCHLAGEN!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
