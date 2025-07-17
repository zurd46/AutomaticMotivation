#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_generator import AIGenerator
from src.job_extractor import JobExtractor
from src.models import JobInfo
from src.intelligent_job_analyzer import JobCategory
from config.config import Config

def test_github_projects_by_category():
    """Teste GitHub-Projekte für verschiedene Stellenkategorien"""
    
    # Mock-Stellenausschreibungen
    test_jobs = [
        {
            "name": "IT-Support",
            "job_info": JobInfo(
                url="https://example.com/it-support",
                company="Test AG",
                position="IT-Support Specialist",
                department="IT",
                address="Zürich",
                contact_person="Max Mustermann",
                description="Verantwortlich für IT-Support, Anwenderbetreuung und Troubleshooting",
                requirements="IT-Support-Erfahrung, Kundenservice, Problemlösung",
                location="Zürich"
            )
        },
        {
            "name": "Software-Entwickler",
            "job_info": JobInfo(
                url="https://example.com/software-dev",
                company="Tech AG",
                position="Software Developer",
                department="Development",
                address="Basel",
                contact_person="Anna Müller",
                description="Softwareentwicklung mit Python, JavaScript und modernen Frameworks",
                requirements="Python, JavaScript, React, Node.js, Git",
                location="Basel"
            )
        }
    ]
    
    ai_generator = AIGenerator()
    personal_info = Config.get_personal_info()
    
    for test_job in test_jobs:
        print(f"\n=== TEST: {test_job['name']} ===")
        
        # Analysiere Job-Kategorie
        job_analysis = ai_generator.job_analyzer.analyze_job(
            test_job['job_info'].position,
            test_job['job_info'].description,
            test_job['job_info'].requirements
        )
        
        print(f"Erkannte Kategorie: {job_analysis['category']}")
        print(f"Confidence: {job_analysis['analysis_confidence']:.2f}")
        
        # Prüfe, ob GitHub-Projekte verwendet werden
        if job_analysis['category'] in [JobCategory.SOFTWARE_DEVELOPMENT, JobCategory.DATA_SCIENCE]:
            print("✅ GitHub-Projekte werden verwendet (Entwickler-Stelle)")
        else:
            print("❌ Keine GitHub-Projekte (Non-Entwickler-Stelle)")
        
        # Teste Motivationsschreiben-Generierung
        try:
            motivation_letter = ai_generator.generate_motivation_letter(
                test_job['job_info'], 
                personal_info
            )
            
            content = motivation_letter.content
            
            # Prüfe auf GitHub-Projekt-Erwähnungen
            github_mentions = [
                'github', 'projekt', 'webp-to-jpg', 'automaticmotivation', 
                'entwickelte', 'implementierte', 'programmierte'
            ]
            
            mentions_found = [mention for mention in github_mentions if mention.lower() in content.lower()]
            
            if mentions_found:
                print(f"⚠️  GitHub-Projekt-Erwähnungen gefunden: {mentions_found}")
            else:
                print("✅ Keine GitHub-Projekt-Erwähnungen gefunden")
                
        except Exception as e:
            print(f"❌ Fehler bei Motivationsschreiben-Generierung: {e}")

if __name__ == "__main__":
    test_github_projects_by_category()
