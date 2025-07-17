#!/usr/bin/env python3
"""
Debug-Script für Job-Extraktion
Testet die Job-Extraktion für IT-Support-Stellen
"""

import sys
sys.path.append('.')

from src.job_extractor import JobExtractor
from src.ai_generator import AIGenerator
import json

def test_job_extraction():
    print("=== Test Job-Extraktion ===")
    
    # Teste mit einer IT-Support URL (Beispiel)
    test_url = input("Bitte geben Sie die IT-Support Job-URL ein: ")
    
    if not test_url:
        print("Keine URL eingegeben - verwende Test-URL")
        return
    
    extractor = JobExtractor()
    
    try:
        print(f"Extrahiere Job-Informationen von: {test_url}")
        job_description = extractor.extract_from_url(test_url)
        
        print("\n=== Extrahierte Job-Informationen ===")
        print(f"Unternehmen: {job_description.company}")
        print(f"Position: {job_description.position}")
        print(f"Abteilung: {job_description.department}")
        print(f"Standort: {job_description.location}")
        print(f"Arbeitszeit: {job_description.working_hours}")
        print(f"Kontaktperson: {job_description.contact_person}")
        
        print(f"\nBeschreibung (erste 200 Zeichen):")
        print(job_description.description[:200] + "...")
        
        print(f"\nAnforderungen (erste 300 Zeichen):")
        print(job_description.requirements[:300] + "...")
        
        print(f"\nVorteile (erste 200 Zeichen):")
        benefits = job_description.benefits or "Keine angegeben"
        print(benefits[:200] + ("..." if len(benefits) > 200 else ""))
        
        # Teste AI-Generator mit den extrahierten Daten
        print("\n=== Teste AI-Generator ===")
        ai_generator = AIGenerator()
        
        # Extrahiere Schlüsselanforderungen
        key_requirements = ai_generator.extract_key_requirements(job_description)
        print(f"Schlüsselanforderungen: {key_requirements}")
        
        # Teste Anrede-Generierung
        salutation = ai_generator._generate_salutation(job_description)
        print(f"Generierte Anrede: {salutation}")
        
        # Analysiere ob es sich um Entwicklung oder IT-Support handelt
        position_lower = job_description.position.lower()
        requirements_lower = job_description.requirements.lower()
        
        print(f"\n=== Positions-Analyse ===")
        print(f"Position enthält 'support': {'support' in position_lower}")
        print(f"Position enthält 'entwickl': {'entwickl' in position_lower}")
        print(f"Position enthält 'developer': {'developer' in position_lower}")
        print(f"Position enthält 'software': {'software' in position_lower}")
        print(f"Position enthält 'IT': {'it' in position_lower}")
        
        print(f"\nAnforderungen enthalten 'support': {'support' in requirements_lower}")
        print(f"Anforderungen enthalten 'entwickl': {'entwickl' in requirements_lower}")
        print(f"Anforderungen enthalten 'programmier': {'programmier' in requirements_lower}")
        print(f"Anforderungen enthalten 'coding': {'coding' in requirements_lower}")
        
    except Exception as e:
        print(f"Fehler bei der Job-Extraktion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_job_extraction()
