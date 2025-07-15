#!/usr/bin/env python3
"""
Erstelle ein einfaches Test-Motivationsschreiben basierend auf dem Template
"""

import sys
import os
from datetime import datetime
from src.models import JobInfo, MotivationLetter
from src.pdf_generator import PDFGenerator
from src.ai_generator import AIGenerator

def create_test_motivation_letter():
    """Erstelle ein Test-Motivationsschreiben"""
    
    # Test-Job-Informationen
    job_info = JobInfo(
        url="https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op",
        company="Datalynx AG",
        position="Software Developer",
        department="IT",
        location="Zürich",
        address="Musterstrasse 123, 8001 Zürich",
        contact_person="Hr. Muster",
        email="hr@datalynx.ch",
        phone="+41 44 123 45 67",
        description="Entwicklung von innovativen Software-Lösungen",
        requirements="Python, JavaScript, Datenbanken, Teamarbeit",
        benefits="Flexible Arbeitszeiten, Homeoffice möglich",
        working_hours="Vollzeit",
        salary="Nach Vereinbarung"
    )
    
    # Persönliche Informationen
    personal_info = {
        'name': 'Daniel Zurmühle',
        'address': 'Hinterdorfstrasse 12, 6235 Winikon',
        'phone': '+41 79 127 55 54',
        'email': 'dzurmuehle@gmail.com',
        'experience': '4 Jahre Berufserfahrung in der Softwareentwicklung',
        'skills': 'Python, Node.js, TypeScript, JAVA, PHP, Datenbanken'
    }
    
    print("🚀 Erstelle Test-Motivationsschreiben...")
    
    try:
        # AI-Generator verwenden
        ai_generator = AIGenerator()
        motivation_letter = ai_generator.generate_motivation_letter(job_info, personal_info)
        
        print(f"✅ Motivationsschreiben generiert für: {job_info.company}")
        
        # PDF erstellen
        pdf_generator = PDFGenerator(template_path="templates/template.pdf")
        pdf_path = pdf_generator.create_pdf(motivation_letter)
        
        print(f"📄 PDF erstellt: {pdf_path}")
        
        # Inhalt anzeigen
        print("\n" + "="*60)
        print("📝 GENERIERTER INHALT:")
        print("="*60)
        print(motivation_letter.content)
        print("="*60)
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None

if __name__ == "__main__":
    create_test_motivation_letter()
