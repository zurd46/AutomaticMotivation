#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.github_project_extractor import GitHubProjectExtractor
from src.job_extractor import JobExtractor
from src.intelligent_job_analyzer import IntelligentJobAnalyzer

def test_improved_project_selection():
    """Teste die verbesserte Projekt-Auswahl-Logik"""
    
    # Test mit IT-Support-Stelle
    print("=== TEST MIT IT-SUPPORT-STELLE ===")
    job_url = "https://jobs.luks.ch/offene-stellen/ict-supporterin-ict-supporter/42918cdb-706b-409d-a4cb-d16e997f8b55"
    
    # Job extrahieren
    job_extractor = JobExtractor()
    job_info = job_extractor.extract_from_url(job_url)
    print(f"Job: {job_info.position}")
    print(f"Beschreibung: {job_info.description[:150]}...")
    
    # Projekte suchen
    github_extractor = GitHubProjectExtractor()
    projects = github_extractor.get_relevant_projects_for_job(
        "https://github.com/zurd46",
        job_info.position,
        job_info.requirements,
        max_projects=3
    )
    
    print(f"\nGefundene Projekte: {len(projects)}")
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project.name} ({project.language})")
        print(f"   Beschreibung: {project.description}")
        print(f"   Topics: {', '.join(project.topics) if project.topics else 'Keine'}")
        print()
    
    # Analyse
    if len(projects) == 0:
        print("✅ ERFOLG: Keine unpassenden Projekte für IT-Support-Stelle ausgewählt!")
    else:
        print(f"⚠️  WARNUNG: {len(projects)} Projekte ausgewählt - prüfe Relevanz:")
        for project in projects:
            print(f"   - {project.name}: {project.description}")

if __name__ == "__main__":
    test_improved_project_selection()
