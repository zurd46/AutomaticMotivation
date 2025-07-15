#!/usr/bin/env python3
"""
Debug Script für LLM-Antwort-Parsing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config.config import Config
import json
from datetime import datetime

def test_llm_response_parsing():
    """Testet die LLM-Antwort-Parsing-Logik"""
    
    print("🔍 Teste LLM-Antwort-Parsing")
    print("=" * 80)
    
    # Beispiel-Text aus der Datalynx-Seite
    sample_text = """
    AI Consultant (m/w/d)
    Zu der Datalynx Gruppe gehören die Unternehmen Datalynx AG, Primetrack AG und skillcloud AG. Sie erbringen IT Dienstleistungen rund um Digitale Lösungen, Quality Management, Helpdesk/Support und Workforce Solutions.

    Zur Verstärkung unseres Teams suchen wir einen AI-Consultant, der unser Unternehmen bei der Entwicklung und Implementierung innovativer Lösungen unterstützt und anspruchsvolle Projekte vorantreibt.

    Aufgaben und Verantwortlichkeiten
    Beratung unserer Kunden bei der Identifikation und Umsetzung von KI-basierten Lösungen zur Optimierung von Geschäftsprozessen

    Allgemeine Informationen
    Start Datum: sofort oder nach Vereinbarung
    Anstellungsart: Festanstellung
    Pensum: 100%
    Arbeitsort: Basel

    Kontakt
    Jan Schmitz-Elsen
    Team Lead Talent Acquisition 
    +41 79 425 10 45
    jan.schmitz@datalynx.ch

    Wir freuen uns auf Deine Online-Bewerbung!
    """
    
    try:
        # LLM konfigurieren
        config = Config.get_llm_config()
        print(f"🔧 LLM Provider: {config['provider']}")
        print(f"🔧 LLM Model: {config['model']}")
        
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
        
        print("✅ LLM initialisiert")
        
        # Prompt erstellen
        prompt = f"""
        Analysiere die folgende Stellenausschreibung und extrahiere die relevanten Informationen:

        TEXT:
        {sample_text}

        Extrahiere folgende Informationen und gib sie in diesem Format zurück:
        
        UNTERNEHMEN: [Name des Unternehmens]
        POSITION: [Stellenbezeichnung]
        BEREICH: [Abteilung/Bereich, falls genannt]
        STANDORT: [Arbeitsort]
        ADRESSE: [Vollständige Adresse des Unternehmens mit Straße, PLZ und Ort]
        KONTAKTPERSON: [Vollständiger Name der Kontaktperson, z.B. "Jan Schmitz-Elsen"]
        KONTAKT_TITEL: [Titel der Kontaktperson, z.B. "Team Lead Talent Acquisition"]
        EMAIL: [E-Mail-Adresse der Kontaktperson]
        TELEFON: [Telefonnummer der Kontaktperson]
        BESCHREIBUNG: [Kurze Beschreibung der Position]
        ANFORDERUNGEN: [Wichtigste Anforderungen]
        BENEFITS: [Angebotene Leistungen]
        ARBEITSZEIT: [Arbeitszeiten, falls genannt]
        GEHALT: [Gehaltsangaben, falls genannt]
        
        WICHTIGE HINWEISE: 
        - Suche im gesamten Text nach "Kontakt", "Ansprechpartner", "Contact" Abschnitten
        - Firmenadresse kann sich aus dem Arbeitsort ableiten lassen
        - Wenn "Arbeitsort: Basel" angegeben ist, dann ist die Adresse "Basel, Schweiz"
        - Kontaktperson steht oft am Ende des Textes oder in einem separaten Kontakt-Bereich
        - Beispiel: "Jan Schmitz-Elsen, Team Lead Talent Acquisition, +41 79 425 10 45, jan.schmitz@datalynx.ch"
        - Wenn keine spezifische Kontaktperson gefunden wird, schreibe "Nicht angegeben"
        - Wenn keine Firmenadresse im Text steht, nutze den Arbeitsort als Adresse
        """
        
        messages = [
            SystemMessage(content="Du bist ein Experte für die Extraktion von Stelleninformationen. Analysiere Stellenausschreibungen präzise und strukturiert."),
            HumanMessage(content=prompt)
        ]
        
        print("\n🤖 Sende Anfrage an LLM...")
        response = llm.invoke(messages)
        
        print("✅ LLM-Antwort erhalten")
        
        # Rohe Antwort anzeigen
        print("\n📄 ROHE LLM-ANTWORT:")
        print("-" * 50)
        print(response.content)
        print("-" * 50)
        
        # Parsing-Logik testen
        def parse_llm_response(response_text: str) -> dict:
            """Parst die LLM-Antwort in ein Dictionary"""
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
        
        parsed_info = parse_llm_response(response.content)
        
        print("\n📊 GEPARSTE INFORMATIONEN:")
        print("=" * 80)
        
        for key, value in parsed_info.items():
            print(f"{key}: {value}")
        
        # Ergebnisse speichern
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"llm_response_{timestamp}.json"
        
        result_data = {
            'prompt': prompt,
            'raw_response': response.content,
            'parsed_info': parsed_info,
            'timestamp': timestamp,
            'llm_config': config
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Ergebnisse gespeichert in: {output_file}")
        
        # Erfolgsanalyse
        print("\n🔍 ERFOLGSANALYSE:")
        print("=" * 80)
        
        success_metrics = {
            'UNTERNEHMEN': parsed_info.get('UNTERNEHMEN'),
            'POSITION': parsed_info.get('POSITION'),
            'KONTAKTPERSON': parsed_info.get('KONTAKTPERSON'),
            'EMAIL': parsed_info.get('EMAIL'),
            'TELEFON': parsed_info.get('TELEFON'),
            'STANDORT': parsed_info.get('STANDORT')
        }
        
        for key, value in success_metrics.items():
            status = "✅" if value else "❌"
            print(f"{status} {key}: {value}")
        
        return parsed_info
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_llm_response_parsing()
