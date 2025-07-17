#!/usr/bin/env python3
"""
Finale Demonstration der RecipientController-Integration
Zeigt die Verbesserungen bei der Empfänger-Behandlung
"""

import os
import sys

# Füge src-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # Für root-level imports

from src.ai_generator import AIGenerator
from src.models import JobDescription
from src.recipient_controller import RecipientController

def demo_recipient_controller():
    """Demonstriert die RecipientController-Funktionalität"""
    print("=== Finale Demonstration: RecipientController ===\n")
    
    # Test-Szenarien
    test_cases = [
        {
            "name": "Szenario 1: Spezifische Kontaktperson (Jan Enz)",
            "job": JobDescription(
                position='ICT Supporterin/ICT Supporter 100%',
                company='Luzerner Kantonsspital',
                contact_person='Jan Enz',
                description='IT-Support Position',
                requirements='IT-Support, Kundenservice',
                benefits='Gute Konditionen',
                location='Luzern',
                address='Luzerner Kantonsspital, Spitalstrasse 1, 6000 Luzern',
                department='IT',
                url='https://example.com',
                working_hours='100%'
            )
        },
        {
            "name": "Szenario 2: Keine Kontaktperson",
            "job": JobDescription(
                position='Software Engineer',
                company='TechCorp AG',
                contact_person='',
                description='Softwareentwicklung',
                requirements='Python, Java',
                benefits='Flexible Arbeitszeiten',
                location='Zürich',
                address='TechCorp AG, Techweg 10, 8000 Zürich',
                department='Development',
                url='https://example.com',
                working_hours='100%'
            )
        },
        {
            "name": "Szenario 3: Generische Kontaktperson (HR Team)",
            "job": JobDescription(
                position='Data Scientist',
                company='DataAnalytics GmbH',
                contact_person='HR Team',
                description='Datenanalyse',
                requirements='Python, Statistics',
                benefits='Spannende Projekte',
                location='Basel',
                address='DataAnalytics GmbH, Datenstrasse 5, 4000 Basel',
                department='Analytics',
                url='https://example.com',
                working_hours='80%'
            )
        },
        {
            "name": "Szenario 4: Keine Kontaktperson, keine Adresse",
            "job": JobDescription(
                position='IT Support Specialist',
                company='StartupXYZ',
                contact_person='',
                description='IT-Support',
                requirements='IT-Kenntnisse',
                benefits='Startup-Atmosphere',
                location='Bern',
                address='',
                department='IT',
                url='https://example.com',
                working_hours='100%'
            )
        }
    ]
    
    controller = RecipientController()
    ai_generator = AIGenerator()
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}")
        print("=" * 50)
        
        job = test_case['job']
        
        # Vor der Normalisierung
        print(f"VOR der Normalisierung:")
        print(f"  Kontaktperson: '{job.contact_person}'")
        print(f"  Adresse: '{job.address}'")
        
        # Normalisierung
        normalized_job = controller.normalize_recipient_info(job)
        validation = controller.validate_recipient_info(job)
        
        print(f"\nNACH der Normalisierung:")
        print(f"  Kontaktperson: '{normalized_job.contact_person}'")
        print(f"  Adresse: '{normalized_job.address}'")
        
        # Anrede-Generierung
        salutation = ai_generator._generate_salutation(normalized_job)
        print(f"  Generierte Anrede: '{salutation}'")
        
        # Validierung
        if validation['warnings']:
            print(f"  Warnungen: {validation['warnings']}")
        if validation['recommendations']:
            print(f"  Empfehlungen: {validation['recommendations']}")
        
        # Zeige Verbesserungen
        improvements = []
        if not job.contact_person and normalized_job.contact_person:
            improvements.append("✅ Kontaktperson automatisch auf Firmenname gesetzt")
        if not job.address and normalized_job.address:
            improvements.append("✅ Standard-Adresse automatisch erstellt")
        if job.contact_person in ['HR Team', 'hr', 'human resources'] and normalized_job.contact_person == job.company:
            improvements.append("✅ Generische Kontaktperson durch Firmenname ersetzt")
        
        if improvements:
            print(f"  Verbesserungen:")
            for improvement in improvements:
                print(f"    {improvement}")
        
        print()
    
    print("=== Zusammenfassung ===")
    print("Der RecipientController bietet folgende Verbesserungen:")
    print("1. Automatisches Fallback auf Firmenname bei fehlender Kontaktperson")
    print("2. Erkennung und Ersetzung generischer Kontaktpersonen (HR Team, etc.)")
    print("3. Automatische Standard-Adresse bei fehlender Firmenadresse")
    print("4. Intelligente Anrede-Generierung basierend auf Kontaktperson-Typ")
    print("5. Bereinigung von Adressen für bessere Kompatibilität")
    print("6. Validierung und Empfehlungen für Empfänger-Informationen")
    print("\nDie Anrede wird jetzt korrekt als 'Sehr geehrte Damen und Herren,' generiert,")
    print("wenn keine spezifische Kontaktperson oder nur eine Firma verfügbar ist.")

if __name__ == "__main__":
    demo_recipient_controller()
