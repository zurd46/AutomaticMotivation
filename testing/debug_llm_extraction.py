#!/usr/bin/env python3
"""
Debug Script für LLM-basierte Job-Extraktion
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.job_extractor import JobExtractor
from config.config import Config
import json
from datetime import datetime

def test_job_extraction():
    """Testet die Job-Extraktion mit der spezifischen URL"""
    url = "https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op"
    
    print(f"🔍 Teste Job-Extraktion für: {url}")
    print("=" * 80)
    
    try:
        # JobExtractor initialisieren
        extractor = JobExtractor()
        print("✅ JobExtractor initialisiert")
        
        # Konfiguration anzeigen
        config = Config.get_llm_config()
        print(f"🔧 LLM Provider: {config['provider']}")
        print(f"🔧 LLM Model: {config['model']}")
        
        # Webseite laden
        print("\n📥 Lade Webseite...")
        html_content = extractor._fetch_webpage(url)
        print(f"✅ HTML geladen ({len(html_content)} Zeichen)")
        
        # Text extrahieren
        print("\n📝 Extrahiere Text aus HTML...")
        clean_text = extractor._extract_text_from_html(html_content)
        print(f"✅ Text extrahiert ({len(clean_text)} Zeichen)")
        
        # Ersten Teil des Textes anzeigen
        print("\n📄 Extrahierter Text (erste 800 Zeichen):")
        print("-" * 50)
        print(clean_text[:800])
        print("-" * 50)
        
        # Strukturierte Extraktion
        print("\n🤖 Führe strukturierte LLM-Extraktion durch...")
        job_info = extractor._extract_structured_info(clean_text, url)
        print("✅ Strukturierte Extraktion abgeschlossen")
        
        # Ergebnisse anzeigen
        print("\n📊 EXTRAKTIONS-ERGEBNISSE:")
        print("=" * 80)
        
        print(f"🏢 Unternehmen: {job_info.company}")
        print(f"💼 Position: {job_info.position}")
        print(f"📍 Standort: {job_info.location}")
        print(f"🏠 Adresse: {job_info.address}")
        print(f"👤 Kontaktperson: {job_info.contact_person}")
        print(f"🎯 Kontakt-Titel: {job_info.contact_title}")
        print(f"📧 Email: {job_info.email}")
        print(f"📞 Telefon: {job_info.phone}")
        print(f"📝 Beschreibung: {job_info.description[:200]}...")
        print(f"📋 Anforderungen: {job_info.requirements[:200]}...")
        print(f"🎁 Benefits: {job_info.benefits}")
        print(f"⏰ Arbeitszeit: {job_info.working_hours}")
        print(f"💰 Gehalt: {job_info.salary}")
        
        # Ergebnisse in Datei speichern
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"job_extraction_{timestamp}.json"
        
        job_data = {
            'url': job_info.url if job_info else None,
            'company': job_info.company if job_info else None,
            'position': job_info.position if job_info else None,
            'location': job_info.location if job_info else None,
            'address': job_info.address if job_info else None,
            'contact_person': job_info.contact_person if job_info else None,
            'contact_title': job_info.contact_title if job_info else None,
            'email': job_info.email if job_info else None,
            'phone': job_info.phone if job_info else None,
            'description': job_info.description if job_info else None,
            'requirements': job_info.requirements if job_info else None,
            'benefits': job_info.benefits if job_info else None,
            'working_hours': job_info.working_hours if job_info else None,
            'salary': job_info.salary if job_info else None,
            'extracted_text': clean_text,
            'extraction_timestamp': timestamp
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Ergebnisse gespeichert in: {output_file}")
        
        # Probleme identifizieren
        print("\n🔍 PROBLEM-ANALYSE:")
        print("=" * 80)
        
        problems = []
        if job_info.company == "Nicht extrahiert" or job_info.company == "Nicht angegeben":
            problems.append("❌ Unternehmen nicht extrahiert")
        if job_info.position == "Nicht extrahiert" or job_info.position == "Nicht angegeben":
            problems.append("❌ Position nicht extrahiert")
        if not job_info.contact_person:
            problems.append("❌ Kontaktperson nicht extrahiert")
        if not job_info.email:
            problems.append("❌ Email nicht extrahiert")
        if not job_info.phone:
            problems.append("❌ Telefonnummer nicht extrahiert")
        if job_info.address == "Nicht extrahiert" or job_info.address == "Nicht angegeben":
            problems.append("❌ Adresse nicht extrahiert")
        
        if problems:
            print("Gefundene Probleme:")
            for problem in problems:
                print(f"  {problem}")
        else:
            print("✅ Alle wichtigen Informationen erfolgreich extrahiert!")
        
        return job_info, clean_text
        
    except Exception as e:
        print(f"❌ Fehler bei der Extraktion: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    test_job_extraction()
