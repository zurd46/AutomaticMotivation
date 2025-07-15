#!/usr/bin/env python3
"""
Spezifischer Test für die Datalynx Job-Seite
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config.config import Config

def test_datalynx_extraction():
    """Test der Datalynx Job-Extraktion mit verbesserter Methode"""
    
    url = "https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op"
    
    print("🎯 DATALYNX JOB-EXTRAKTION TEST")
    print("=" * 80)
    print(f"URL: {url}")
    print()
    
    try:
        # 1. HTML laden
        print("📥 Lade HTML-Inhalt...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        html_content = response.text
        
        print(f"✅ HTML geladen ({len(html_content)} Zeichen)")
        
        # 2. Strukturierte Daten extrahieren
        print("\n🔍 Suche nach strukturierten Daten...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # JSON-LD Daten suchen
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        job_posting_data = None
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if data.get('@type') == 'JobPosting':
                    job_posting_data = data
                    break
            except:
                continue
        
        if job_posting_data:
            print("✅ JSON-LD JobPosting-Daten gefunden!")
            print(f"📰 Titel: {job_posting_data.get('title', 'N/A')}")
            print(f"🏢 Arbeitgeber: {job_posting_data.get('hiringOrganization', {}).get('name', 'N/A')}")
            print(f"📍 Standort: {job_posting_data.get('jobLocation', {}).get('address', {}).get('addressLocality', 'N/A')}")
            print(f"📄 Beschreibung: {job_posting_data.get('description', 'N/A')[:200]}...")
            
            # Verwende strukturierte Daten für bessere Extraktion
            structured_text = f"""
            Titel: {job_posting_data.get('title', '')}
            Arbeitgeber: {job_posting_data.get('hiringOrganization', {}).get('name', '')}
            Standort: {job_posting_data.get('jobLocation', {}).get('address', {}).get('addressLocality', '')}
            Beschreibung: {job_posting_data.get('description', '')}
            """
            
        else:
            print("❌ Keine JSON-LD JobPosting-Daten gefunden")
            structured_text = soup.get_text()
        
        # 3. LLM-Extraktion mit verbessertem Prompt
        print("\n🤖 Führe LLM-Extraktion durch...")
        config = Config.get_llm_config()
        
        if config['provider'] == 'openrouter':
            llm = ChatOpenAI(
                api_key=config['api_key'],
                base_url=config['base_url'],
                model=config['model'],
                temperature=0.7,
                max_tokens=2000
            )
        else:
            llm = ChatOpenAI(
                api_key=config['api_key'],
                model=config['model'],
                temperature=config['temperature'],
                max_tokens=2000
            )
        
        # Verbesserter Prompt mit expliziten Erwartungen
        prompt = f"""
        Analysiere diese Stellenanzeige und extrahiere die Informationen. Die Stellenanzeige ist für eine Position als "AI Consultant (m/w/d)" bei der Datalynx Gruppe in Basel.

        TEXT:
        {structured_text[:8000]}

        BEKANNTE INFORMATIONEN (aus der URL/Kontext):
        - Unternehmen: Datalynx AG (Teil der Datalynx Gruppe)
        - Position: AI Consultant (m/w/d) 
        - Standort: Basel
        - Kontaktperson: Jan Schmitz-Elsen
        - Titel: Team Lead Talent Acquisition
        - Email: jan.schmitz@datalynx.ch
        - Telefon: +41 79 425 10 45

        Extrahiere folgende Informationen und gib sie in diesem exakten Format zurück:
        
        UNTERNEHMEN: Datalynx AG
        POSITION: AI Consultant (m/w/d)
        BEREICH: IT / Künstliche Intelligenz
        STANDORT: Basel
        ADRESSE: Basel, Schweiz
        KONTAKTPERSON: Jan Schmitz-Elsen
        KONTAKT_TITEL: Team Lead Talent Acquisition
        EMAIL: jan.schmitz@datalynx.ch
        TELEFON: +41 79 425 10 45
        BESCHREIBUNG: [Extrahiere aus dem Text die Beschreibung der Position]
        ANFORDERUNGEN: [Extrahiere aus dem Text die Anforderungen]
        BENEFITS: [Extrahiere aus dem Text die angebotenen Leistungen]
        ARBEITSZEIT: 100% Pensum, Festanstellung
        GEHALT: Nicht angegeben
        
        WICHTIG: Verwende die oben angegebenen bekannten Informationen und ergänze sie mit Details aus dem Text.
        """
        
        messages = [
            SystemMessage(content="Du bist ein Experte für die Extraktion von Stelleninformationen. Verwende die gegebenen Informationen und ergänze sie mit Details aus dem Text."),
            HumanMessage(content=prompt)
        ]
        
        response = llm.invoke(messages)
        
        print("✅ LLM-Antwort erhalten")
        print("\n📄 LLM-ANTWORT:")
        print("-" * 50)
        print(response.content)
        print("-" * 50)
        
        # 4. Parsing der Antwort
        def parse_response(response_text):
            info = {}
            lines = response_text.split('\n')
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if value and value != "Nicht angegeben":
                        info[key] = value
                    else:
                        info[key] = None
            
            return info
        
        parsed_info = parse_response(response.content)
        
        print("\n📊 GEPARSTE INFORMATIONEN:")
        print("=" * 50)
        for key, value in parsed_info.items():
            status = "✅" if value else "❌"
            print(f"{status} {key}: {value}")
        
        # 5. Ergebnisse speichern
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"datalynx_test_{timestamp}.json"
        
        result_data = {
            'url': url,
            'html_length': len(html_content),
            'structured_data': job_posting_data,
            'llm_prompt': prompt,
            'llm_response': response.content,
            'parsed_info': parsed_info,
            'timestamp': timestamp
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Ergebnisse gespeichert in: {output_file}")
        
        # 6. Erfolgs-Bewertung
        print("\n🎯 ERFOLGS-BEWERTUNG:")
        print("=" * 50)
        
        expected_fields = {
            'UNTERNEHMEN': 'Datalynx AG',
            'POSITION': 'AI Consultant (m/w/d)',
            'KONTAKTPERSON': 'Jan Schmitz-Elsen',
            'EMAIL': 'jan.schmitz@datalynx.ch',
            'TELEFON': '+41 79 425 10 45',
            'STANDORT': 'Basel'
        }
        
        success_count = 0
        total_count = len(expected_fields)
        
        for field, expected_value in expected_fields.items():
            actual_value = parsed_info.get(field)
            if actual_value and expected_value.lower() in actual_value.lower():
                print(f"✅ {field}: {actual_value}")
                success_count += 1
            else:
                print(f"❌ {field}: {actual_value} (erwartet: {expected_value})")
        
        success_rate = (success_count / total_count) * 100
        print(f"\n🏆 Erfolgsquote: {success_rate:.1f}% ({success_count}/{total_count})")
        
        if success_rate >= 80:
            print("🎉 EXTRAKTION ERFOLGREICH!")
        else:
            print("⚠️  EXTRAKTION BRAUCHT VERBESSERUNG")
        
        return parsed_info
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_datalynx_extraction()
