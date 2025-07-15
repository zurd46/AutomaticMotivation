#!/usr/bin/env python3
"""
Debug Script für HTML-Extraktion von Job-Informationen
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

def fetch_webpage(url: str) -> str:
    """Lädt den HTML-Inhalt einer Webseite"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text

def analyze_html_structure(html_content: str) -> dict:
    """Analysiert die HTML-Struktur nach Job-Informationen"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    analysis = {
        'title': None,
        'contact_info': [],
        'company_info': [],
        'email_addresses': [],
        'phone_numbers': [],
        'addresses': [],
        'structured_data': [],
        'meta_data': [],
        'raw_text': None
    }
    
    # 1. Title extrahieren
    title_tag = soup.find('title')
    if title_tag:
        analysis['title'] = title_tag.get_text().strip()
    
    # 2. Meta-Daten extrahieren
    meta_tags = soup.find_all('meta')
    for meta in meta_tags:
        if meta.get('name') or meta.get('property'):
            analysis['meta_data'].append({
                'name': meta.get('name') or meta.get('property'),
                'content': meta.get('content')
            })
    
    # 3. Strukturierte Daten (JSON-LD, Microdata)
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            analysis['structured_data'].append(data)
        except:
            pass
    
    # 4. Email-Adressen suchen
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_links = soup.find_all('a', href=re.compile(r'mailto:'))
    for link in email_links:
        email = link.get('href').replace('mailto:', '')
        analysis['email_addresses'].append(email)
    
    # Im Text nach Emails suchen
    text_content = soup.get_text()
    emails_in_text = re.findall(email_pattern, text_content)
    analysis['email_addresses'].extend(emails_in_text)
    
    # 5. Telefonnummern suchen
    phone_pattern = r'(\+41\s?)?(\d{2}\s?\d{3}\s?\d{2}\s?\d{2}|\d{3}\s?\d{3}\s?\d{2}\s?\d{2})'
    tel_links = soup.find_all('a', href=re.compile(r'tel:'))
    for link in tel_links:
        phone = link.get('href').replace('tel:', '')
        analysis['phone_numbers'].append(phone)
    
    # Im Text nach Telefonnummern suchen
    phones_in_text = re.findall(phone_pattern, text_content)
    analysis['phone_numbers'].extend([f"{p[0]}{p[1]}" for p in phones_in_text])
    
    # 6. Kontakt-Bereiche finden
    contact_sections = soup.find_all(text=re.compile(r'(kontakt|contact|ansprechpartner)', re.IGNORECASE))
    for section in contact_sections:
        parent = section.parent
        if parent:
            analysis['contact_info'].append(parent.get_text().strip())
    
    # 7. Firmen-Informationen
    company_indicators = soup.find_all(text=re.compile(r'(ag|gmbh|ltd|inc|corp)', re.IGNORECASE))
    for indicator in company_indicators[:5]:  # Nur erste 5
        parent = indicator.parent
        if parent:
            analysis['company_info'].append(parent.get_text().strip())
    
    # 8. Adress-Informationen
    address_patterns = [
        r'\d{4,5}\s+[A-Za-z\s]+',  # PLZ + Ort
        r'[A-Za-z\s]+\s+\d+',      # Straße + Hausnummer
    ]
    
    for pattern in address_patterns:
        addresses = re.findall(pattern, text_content)
        analysis['addresses'].extend(addresses)
    
    # 9. Rohen Text speichern (gekürzt)
    analysis['raw_text'] = text_content[:2000]
    
    return analysis

def debug_specific_url():
    """Debug die spezifische URL"""
    url = "https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op"
    
    print(f"🔍 Analysiere URL: {url}")
    print("=" * 80)
    
    try:
        # HTML laden
        html_content = fetch_webpage(url)
        print(f"✅ HTML erfolgreich geladen ({len(html_content)} Zeichen)")
        
        # Analysieren
        analysis = analyze_html_structure(html_content)
        
        # Ergebnisse ausgeben
        print("\n📊 ANALYSE ERGEBNISSE:")
        print("=" * 80)
        
        print(f"📰 Title: {analysis['title']}")
        
        print(f"\n📧 Email-Adressen gefunden: {len(analysis['email_addresses'])}")
        for email in set(analysis['email_addresses']):
            print(f"  - {email}")
        
        print(f"\n📞 Telefonnummern gefunden: {len(analysis['phone_numbers'])}")
        for phone in set(analysis['phone_numbers']):
            print(f"  - {phone}")
        
        print(f"\n👥 Kontakt-Bereiche gefunden: {len(analysis['contact_info'])}")
        for i, contact in enumerate(analysis['contact_info'][:3]):
            print(f"  {i+1}. {contact[:100]}...")
        
        print(f"\n🏢 Firmen-Informationen gefunden: {len(analysis['company_info'])}")
        for i, company in enumerate(analysis['company_info'][:3]):
            print(f"  {i+1}. {company[:100]}...")
        
        print(f"\n📍 Adressen gefunden: {len(analysis['addresses'])}")
        for address in set(analysis['addresses'][:5]):
            print(f"  - {address}")
        
        print(f"\n🔗 Strukturierte Daten gefunden: {len(analysis['structured_data'])}")
        for i, data in enumerate(analysis['structured_data']):
            print(f"  {i+1}. {str(data)[:100]}...")
        
        print(f"\n📋 Meta-Daten gefunden: {len(analysis['meta_data'])}")
        for meta in analysis['meta_data'][:5]:
            print(f"  - {meta['name']}: {meta['content']}")
        
        print(f"\n📄 Roher Text (erste 500 Zeichen):")
        print("-" * 50)
        print(analysis['raw_text'][:500])
        
        # Ergebnisse in Datei speichern
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"html_analysis_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Analyse gespeichert in: {output_file}")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    debug_specific_url()
