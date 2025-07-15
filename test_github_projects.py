#!/usr/bin/env python3
"""
Test-Skript für die erweiterte AI-Generierung mit GitHub-Projekten
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.github_project_extractor import GitHubProjectExtractor
from config.config import Config

def test_github_extraction():
    """Test der GitHub-Projekt-Extraktion"""
    
    # Persönliche Informationen laden
    personal_info = Config.get_personal_info()
    github_url = personal_info['github']
    
    print(f"GitHub-URL: {github_url}")
    print("=" * 50)
    
    # GitHub-Extraktor initialisieren
    extractor = GitHubProjectExtractor()
    
    # Projekte abrufen
    print("1. Rufe GitHub-Projekte ab...")
    projects = extractor.get_github_projects(github_url)
    
    if projects:
        print(f"✓ Erfolgreich {len(projects)} Projekte abgerufen")
        print("\nTop 5 Projekte:")
        for i, project in enumerate(projects[:5]):
            print(f"  {i+1}. {project.name} ({project.language}) - {project.stars} Sterne")
            print(f"     Beschreibung: {project.description}")
            print(f"     Topics: {', '.join(project.topics) if project.topics else 'Keine'}")
            print()
    else:
        print("✗ Keine Projekte gefunden")
        return
    
    # Test der Projekt-Auswahl für AI Consultant
    print("2. Teste Projekt-Auswahl für AI Consultant...")
    job_position = "AI Consultant"
    job_requirements = "Python, Machine Learning, KI-Entwicklung, Automatisierung, Beratung"
    
    relevant_projects = extractor.select_relevant_projects(
        projects, job_position, job_requirements, max_projects=3
    )
    
    if relevant_projects:
        print(f"✓ {len(relevant_projects)} relevante Projekte ausgewählt:")
        for i, project in enumerate(relevant_projects):
            print(f"  {i+1}. {project.name} ({project.language})")
            print(f"     Beschreibung: {project.description}")
            print(f"     Topics: {', '.join(project.topics) if project.topics else 'Keine'}")
            print(f"     URL: {project.url}")
            print()
        
        # Formatierung für Bewerbung
        formatted = extractor.format_projects_for_application(relevant_projects)
        print("3. Formatierte Projekte für Bewerbung:")
        print(formatted)
    else:
        print("✗ Keine relevanten Projekte gefunden")

if __name__ == "__main__":
    test_github_extraction()
