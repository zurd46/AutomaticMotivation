#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_generator import AIGenerator
from src.job_extractor import JobExtractor
from src.intelligent_job_analyzer import IntelligentJobAnalyzer
import json

def analyze_generated_content():
    """Analysiere den generierten Inhalt des Motivationsschreibens"""
    
    # Job-URL
    job_url = "https://jobs.luks.ch/offene-stellen/ict-supporterin-ict-supporter/42918cdb-706b-409d-a4cb-d16e997f8b55"
    
    # Extrahiere Job-Informationen
    print("=== EXTRAHIERE JOB-INFORMATIONEN ===")
    job_extractor = JobExtractor()
    job_info = job_extractor.extract_from_url(job_url)
    
    print(f"Job-Position: {job_info.position}")
    print(f"Unternehmen: {job_info.company}")
    print(f"Beschreibung (erste 300 Zeichen): {job_info.description[:300]}...")
    
    # Analysiere Job-Kategorie
    print("\n=== ANALYSIERE JOB-KATEGORIE ===")
    analyzer = IntelligentJobAnalyzer()
    job_analysis = analyzer.analyze_job(job_info.position, job_info.description, job_info.requirements)
    
    print(f"Erkannte Kategorie: {job_analysis['category']}")
    print(f"Confidence: {job_analysis['analysis_confidence']:.2f}")
    print(f"Fokus-Bereiche: {job_analysis['focus_recommendations']}")
    print(f"Hauptaufgaben: {job_analysis['main_tasks']}")
    print(f"Relevante Skills: {job_analysis['relevant_skills']}")
    
    # Persönliche Informationen
    print("\n=== PERSÖNLICHE INFORMATIONEN ===")
    personal_info = {
        'name': 'Daniel Zurmühle',
        'address': 'Hinterdorfstrasse 12, 6235 Winikon',
        'phone': '+41 79 127 55 54',
        'email': 'dzurmuehle@gmail.com',
        'github': 'https://github.com/zurd46',
        'linkedin': 'https://www.linkedin.com/in/zurd46',
        'experience': '4+ Jahre Berufserfahrung',
        'skills': 'Python, Node.js, TypeScript, JAVA, PHP, LangChain, OpenAI, OpenRouter, AI-Generierung, AI Agent Systeme, Automatisierung, Webentwicklung, Datenanalyse'
    }
    
    # Generiere Motivationsschreiben
    print("\n=== GENERIERE MOTIVATIONSSCHREIBEN ===")
    ai_generator = AIGenerator()
    motivation_text = ai_generator.generate_motivation_letter(job_info, personal_info)
    
    # Extrahiere den Text aus der MotivationLetter-Struktur
    motivation_content = motivation_text.content
    
    print("=== GENERIERTES MOTIVATIONSSCHREIBEN ===")
    print(motivation_content)
    
    # Analyse des generierten Textes
    print("\n=== INHALTSANALYSE ===")
    
    # Prüfe auf IT-Support relevante Begriffe
    it_support_keywords = ['support', 'betreuung', 'wartung', 'installation', 'troubleshooting', 'hilfe', 'anwender', 'benutzer', 'system', 'servicegedanken', 'first-level', 'ticketing']
    development_keywords = ['entwicklung', 'programmierung', 'software entwickeln', 'code', 'implementierung', 'entwickeln', 'programming', 'framework']
    
    it_support_count = sum(1 for keyword in it_support_keywords if keyword.lower() in motivation_content.lower())
    development_count = sum(1 for keyword in development_keywords if keyword.lower() in motivation_content.lower())
    
    print(f"IT-Support Keywords gefunden: {it_support_count}")
    print(f"Development Keywords gefunden: {development_count}")
    
    # Spezifische Phrasen prüfen
    it_support_phrases = ['first-level-support', 'anwenderbetreuung', 'kundenservice', 'problemlösung', 'servicegedanken', 'hands-on', 'arbeitsplatzsysteme', 'peripheriegeräte']
    development_phrases = ['software entwickeln', 'programmieren', 'code entwickeln', 'implementieren', 'software development']
    
    it_phrases_found = [phrase for phrase in it_support_phrases if phrase in motivation_content.lower()]
    dev_phrases_found = [phrase for phrase in development_phrases if phrase in motivation_content.lower()]
    
    print(f"IT-Support Phrasen gefunden: {it_phrases_found}")
    print(f"Development Phrasen gefunden: {dev_phrases_found}")
    
    if it_support_count > development_count:
        print("✅ ERFOLG: Motivationsschreiben ist IT-Support-fokussiert!")
    else:
        print("❌ PROBLEM: Motivationsschreiben ist immer noch development-fokussiert!")
    
    return motivation_content

if __name__ == "__main__":
    analyze_generated_content()
