#!/usr/bin/env python3
"""
Test-Skript für ultra-spezifische AI-Generierung mit konkreten Kennzahlen
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import JobDescription
from src.ai_generator import AIGenerator
from config.config import Config

def test_ultra_specific_ai():
    """Test der ultra-spezifischen AI-Generierung"""
    
    # Sehr spezifische Stellenbeschreibung
    job_description = JobDescription(
        url="https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op",
        company="Datalynx AG",
        position="Senior AI Consultant",
        department="Data Science & AI Solutions",
        description="""
        Entwicklung und Implementierung von KI-Lösungen für Unternehmenskunden.
        Beratung von C-Level Executives bei AI-Strategien. Leitung von Projektteams
        mit 3-8 Mitarbeitern. Durchführung von Workshops und Präsentationen.
        """,
        requirements="""
        - 4+ Jahre Erfahrung in Python, Machine Learning, Deep Learning
        - Expertise in OpenAI APIs, LangChain, TensorFlow/PyTorch
        - Erfahrung mit LLMs und Natural Language Processing
        - Projektmanagement und Teamleitung (3-8 Personen)
        - Kundenberatung und Präsentationsfähigkeiten
        - Agile/Scrum Methodiken
        - Fintech oder Consulting Hintergrund von Vorteil
        """,
        benefits="120k-150k CHF, Homeoffice, Weiterbildungsbudget 5k CHF",
        contact_person="Dr. Sarah Weber",
        address="Bahnhofstrasse 45, 8001 Zürich, Schweiz",
        location="Zürich",
        working_hours="100% (Vollzeit)"
    )
    
    # AI-Generator mit erweiterten Einstellungen
    generator = AIGenerator()
    personal_info = Config.get_personal_info()
    
    print("=" * 70)
    print("TEST: ULTRA-SPEZIFISCHE AI-GENERIERUNG")
    print("=" * 70)
    print(f"Position: {job_description.position}")
    print(f"Unternehmen: {job_description.company}")
    print(f"Kontakt: {job_description.contact_person}")
    print(f"Spezifische Anforderungen: Fintech, Teamleitung, C-Level Beratung")
    print("=" * 70)
    
    try:
        # Generiere ultra-spezifische Bewerbung
        print("Generiere ultra-spezifische Bewerbung...")
        motivation_letter = generator.generate_motivation_letter(job_description, personal_info)
        
        print("✓ Ultra-spezifische Bewerbung erfolgreich generiert!")
        print("\n" + "=" * 70)
        print("ULTRA-SPEZIFISCHE BEWERBUNG:")
        print("=" * 70)
        print(f"Empfänger: {motivation_letter.recipient_name}")
        print(f"Firma: {motivation_letter.recipient_company}")
        print(f"Betreff: {motivation_letter.subject}")
        print("\nInhalt:")
        print("-" * 50)
        print(motivation_letter.content)
        print("-" * 50)
        
        # Erweiterte Analyse
        content = motivation_letter.content.lower()
        
        # Prüfe auf spezifische Kennzahlen
        kennzahlen_keywords = ['%', 'prozent', 'stunden', 'tage', 'wochen', 'monate', 'personen', 'mitarbeiter', 'kunden', 'projekte', 'chf', 'euro', 'dollar']
        found_kennzahlen = [kw for kw in kennzahlen_keywords if kw in content]
        
        # Prüfe auf Teamarbeit/Leadership
        team_keywords = ['team', 'leitung', 'führung', 'workshop', 'präsentation', 'stakeholder', 'kunde', 'beratung']
        found_team = [kw for kw in team_keywords if kw in content]
        
        # Prüfe auf Technologien
        tech_keywords = ['python', 'machine learning', 'ai', 'ki', 'openai', 'langchain', 'tensorflow', 'pytorch']
        found_tech = [kw for kw in tech_keywords if kw in content]
        
        # Prüfe auf Branchen
        industry_keywords = ['fintech', 'banking', 'finance', 'consulting', 'beratung', 'data science']
        found_industry = [kw for kw in industry_keywords if kw in content]
        
        word_count = len(motivation_letter.content.split())
        
        print(f"\n📊 ANALYSE DER SPEZIFITÄT:")
        print(f"✓ Wortanzahl: {word_count} Wörter")
        print(f"✓ Kennzahlen gefunden: {len(found_kennzahlen)} ({', '.join(found_kennzahlen)})")
        print(f"✓ Team/Leadership Begriffe: {len(found_team)} ({', '.join(found_team)})")
        print(f"✓ Technologie-Begriffe: {len(found_tech)} ({', '.join(found_tech)})")
        print(f"✓ Branchen-Begriffe: {len(found_industry)} ({', '.join(found_industry)})")
        
        # Bewertung der Spezifität
        specificity_score = (len(found_kennzahlen) * 2) + len(found_team) + len(found_tech) + len(found_industry)
        print(f"\n🎯 SPEZIFITÄTS-SCORE: {specificity_score}/20")
        
        if specificity_score >= 15:
            print("🟢 EXZELLENT - Sehr spezifische Bewerbung!")
        elif specificity_score >= 10:
            print("🟡 GUT - Gute Spezifität, aber noch Verbesserungspotential")
        else:
            print("🔴 VERBESSERUNGSBEDARF - Bewerbung zu generisch")
        
        print("\n" + "=" * 70)
        print("ULTRA-SPEZIFISCHER TEST ABGESCHLOSSEN")
        print("=" * 70)
        
    except Exception as e:
        print(f"✗ Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ultra_specific_ai()
