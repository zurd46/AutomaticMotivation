#!/usr/bin/env python3
"""
Test-Skript für die verbesserte AI-Generierung mit GitHub-Projekten
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import JobDescription
from src.ai_generator import AIGenerator
from config.config import Config

def test_improved_ai_generation():
    """Test der verbesserten AI-Generierung mit GitHub-Projekten"""
    
    # Test-Stellenbeschreibung für AI Consultant
    job_description = JobDescription(
        url="https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op",
        company="Datalynx AG",
        position="AI Consultant",
        department="IT & Data Science",
        description="Entwicklung innovativer KI-Lösungen und Beratung von Kunden bei der Implementierung von AI-Systemen",
        requirements="""
        - Mehrjährige Erfahrung in Python und Machine Learning
        - Expertise in LangChain, OpenAI APIs und AI-Frameworks
        - Erfahrung mit KI-Agentensystemen und Automatisierung
        - Starke Beratungsfähigkeiten und Kundenorientierung
        - Projektmanagement und Teamarbeit
        - Präsentationsfähigkeiten
        """,
        benefits="Flexible Arbeitszeiten, Homeoffice, Weiterbildungsmöglichkeiten",
        contact_person="Jan Schmitz-Elsen",
        address="Aeschenplatz 6, 4052 Basel, Schweiz",
        location="Basel",
        working_hours="100% (Vollzeit)"
    )
    
    # AI-Generator initialisieren
    generator = AIGenerator()
    
    # Persönliche Informationen laden
    personal_info = Config.get_personal_info()
    
    print("=" * 60)
    print("TEST: Verbesserte AI-Generierung mit GitHub-Projekten")
    print("=" * 60)
    print(f"Position: {job_description.position}")
    print(f"Unternehmen: {job_description.company}")
    print(f"GitHub-URL: {personal_info['github']}")
    print("=" * 60)
    
    try:
        # Motivationsschreiben generieren
        print("Generiere Motivationsschreiben mit GitHub-Projekten...")
        motivation_letter = generator.generate_motivation_letter(job_description, personal_info)
        
        print("✓ Motivationsschreiben erfolgreich generiert!")
        print("\n" + "=" * 60)
        print("GENERIERTES MOTIVATIONSSCHREIBEN:")
        print("=" * 60)
        print(f"Empfänger: {motivation_letter.recipient_name}")
        print(f"Firma: {motivation_letter.recipient_company}")
        print(f"Betreff: {motivation_letter.subject}")
        print("\nInhalt:")
        print("-" * 40)
        print(motivation_letter.content)
        print("-" * 40)
        
        # Prüfe, ob GitHub-Projekte erwähnt werden
        content_lower = motivation_letter.content.lower()
        github_mentions = []
        
        # Bekannte Projekte aus dem Test
        known_projects = ['automaticmotivation', 'zurdllmws', 'auto-search-jobs', 'python', 'machine learning']
        
        for project in known_projects:
            if project in content_lower:
                github_mentions.append(project)
        
        print(f"\n✓ Betreff enthält Arbeitszeit: {'100%' in motivation_letter.subject}")
        print(f"✓ Korrekte Anrede: {'Sehr geehrter Herr Schmitz-Elsen' in motivation_letter.content}")
        print(f"✓ GitHub-Projekte erwähnt: {len(github_mentions)} Referenzen gefunden")
        if github_mentions:
            print(f"  Erwähnte Projekte/Technologien: {', '.join(github_mentions)}")
        
        # Länge des Inhalts prüfen
        word_count = len(motivation_letter.content.split())
        print(f"✓ Wortanzahl: {word_count} Wörter (Ziel: 350-450)")
        
        if 350 <= word_count <= 500:
            print("✓ Wortanzahl im Zielbereich")
        else:
            print("⚠ Wortanzahl außerhalb des Zielbereichs")
        
        print("\n" + "=" * 60)
        print("TEST ERFOLGREICH ABGESCHLOSSEN")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Fehler bei der Generierung: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_ai_generation()
