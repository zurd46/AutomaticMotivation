#!/usr/bin/env python3
"""
Erstelle ein vollständiges Test-System, das die Job-URL verarbeitet
"""

import sys
import os
from datetime import datetime
from src.models import JobInfo, MotivationLetter
from src.pdf_generator import PDFGenerator
from src.ai_generator import AIGenerator

def create_manual_job_info():
    """Erstelle manuell Job-Informationen basierend auf der URL"""
    
    print("📋 Erstelle Job-Informationen manuell...")
    
    # Diese Informationen würden normalerweise aus der URL extrahiert
    job_info = JobInfo(
        url="https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op",
        company="Datalynx AG",
        position="Senior Software Developer",
        department="Development Team",
        location="Zürich, Schweiz",
        address="Technopark Zürich, Technoparkstrasse 1, 8005 Zürich",
        contact_person="Personal Team",
        email="jobs@datalynx.ch",
        phone="+41 44 632 42 42",
        description="Als Senior Software Developer entwickeln Sie innovative Lösungen für unsere Data-Analytics-Plattform. Sie arbeiten in einem agilen Team und sind verantwortlich für die Architektur und Implementierung von skalierbaren Anwendungen.",
        requirements="Mehrjährige Erfahrung in der Softwareentwicklung, Kenntnisse in Python, JavaScript, Node.js, Datenbanken (SQL/NoSQL), Agile Methoden, Teamarbeit, Problemlösungsfähigkeiten",
        benefits="Flexible Arbeitszeiten, Homeoffice-Möglichkeit, Weiterbildungsmöglichkeiten, attraktive Sozialleistungen, modernste Arbeitsplätze",
        working_hours="Vollzeit (40h/Woche)",
        salary="CHF 90'000 - 110'000 je nach Erfahrung"
    )
    
    print(f"✅ Job-Info erstellt: {job_info.company} - {job_info.position}")
    return job_info

def create_full_motivation_letter():
    """Erstelle ein vollständiges Motivationsschreiben"""
    
    print("🚀 Starte vollständige Motivationsschreiben-Erstellung...")
    print("="*60)
    
    # Job-Informationen
    job_info = create_manual_job_info()
    
    # Persönliche Informationen
    personal_info = {
        'name': 'Daniel Zurmühle',
        'address': 'Hinterdorfstrasse 12, 6235 Winikon',
        'phone': '+41 79 127 55 54',
        'email': 'dzurmuehle@gmail.com',
        'experience': '4 Jahre Berufserfahrung in der Softwareentwicklung mit Fokus auf Python, JavaScript und Datenbanken',
        'skills': 'Python, Node.js, TypeScript, JAVA, PHP, PostgreSQL, MongoDB, React, Vue.js, Docker, Git, Agile Entwicklung'
    }
    
    print(f"👤 Bewerber: {personal_info['name']}")
    print(f"📍 Adresse: {personal_info['address']}")
    print(f"📧 E-Mail: {personal_info['email']}")
    print(f"📞 Telefon: {personal_info['phone']}")
    
    try:
        # AI-Generator verwenden
        print("\n🤖 Generiere Motivationsschreiben mit KI...")
        ai_generator = AIGenerator()
        motivation_letter = ai_generator.generate_motivation_letter(job_info, personal_info)
        
        print(f"✅ Motivationsschreiben generiert")
        
        # PDF erstellen
        print("\n📄 Erstelle PDF-Dokument...")
        pdf_generator = PDFGenerator(template_path="templates/template.pdf")
        
        # Template-Analyse anzeigen
        template_analysis = pdf_generator.analyze_template("templates/template.pdf")
        if template_analysis.get("template_found"):
            print(f"✅ Template gefunden: {template_analysis.get('file_size', 0)} Bytes")
            if template_analysis.get("error"):
                print(f"⚠️  Template-Warnung: {template_analysis.get('error')}")
        else:
            print("❌ Template nicht gefunden - verwende Standard-Format")
        
        pdf_path = pdf_generator.create_pdf(motivation_letter)
        
        print(f"📄 PDF erstellt: {pdf_path}")
        
        # Zusammenfassung
        print("\n" + "="*60)
        print("🎉 ERFOLGREICH ABGESCHLOSSEN!")
        print("="*60)
        print(f"📋 Unternehmen: {job_info.company}")
        print(f"💼 Position: {job_info.position}")
        print(f"📍 Standort: {job_info.location}")
        print(f"👤 Bewerber: {personal_info['name']}")
        print(f"📄 PDF-Datei: {pdf_path}")
        print(f"📊 Dateigröße: {os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0} Bytes")
        
        # Inhalt anzeigen
        print(f"\n📝 GENERIERTER INHALT (erste 200 Zeichen):")
        print("-" * 40)
        print(motivation_letter.content[:200] + "..." if len(motivation_letter.content) > 200 else motivation_letter.content)
        print("-" * 40)
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    create_full_motivation_letter()
