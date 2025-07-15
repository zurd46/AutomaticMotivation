#!/usr/bin/env python3
"""
Master Test Script für Job-Extraktion Debugging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import json

def run_all_tests():
    """Führt alle Tests aus"""
    print("🚀 AUTOMOTI - JOB EXTRAKTION DEBUG SUITE")
    print("=" * 80)
    print(f"📅 Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL: https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op")
    print()
    
    results = {}
    
    # Test 1: HTML-Analyse
    print("🔍 TEST 1: HTML-STRUKTUR-ANALYSE")
    print("-" * 50)
    try:
        from debug_html_extraction import debug_specific_url
        debug_specific_url()
        results['html_analysis'] = "✅ Erfolgreich"
    except Exception as e:
        print(f"❌ Fehler bei HTML-Analyse: {e}")
        results['html_analysis'] = f"❌ Fehler: {e}"
    
    print("\n" + "=" * 80)
    
    # Test 2: LLM-Parsing-Test
    print("🔍 TEST 2: LLM-ANTWORT-PARSING")
    print("-" * 50)
    try:
        from debug_llm_parsing import test_llm_response_parsing
        parsed_info = test_llm_response_parsing()
        if parsed_info:
            results['llm_parsing'] = "✅ Erfolgreich"
            results['llm_data'] = parsed_info
        else:
            results['llm_parsing'] = "❌ Keine Daten"
    except Exception as e:
        print(f"❌ Fehler bei LLM-Parsing: {e}")
        results['llm_parsing'] = f"❌ Fehler: {e}"
    
    print("\n" + "=" * 80)
    
    # Test 3: Komplette Job-Extraktion
    print("🔍 TEST 3: KOMPLETTE JOB-EXTRAKTION")
    print("-" * 50)
    try:
        from debug_llm_extraction import test_job_extraction
        job_info, clean_text = test_job_extraction()
        if job_info:
            results['job_extraction'] = "✅ Erfolgreich"
            results['job_data'] = {
                'company': job_info.company,
                'position': job_info.position,
                'contact_person': job_info.contact_person,
                'email': job_info.email,
                'phone': job_info.phone,
                'address': job_info.address
            }
        else:
            results['job_extraction'] = "❌ Keine Daten"
    except Exception as e:
        print(f"❌ Fehler bei Job-Extraktion: {e}")
        results['job_extraction'] = f"❌ Fehler: {e}"
    
    print("\n" + "=" * 80)
    
    # Zusammenfassung
    print("📊 TEST-ZUSAMMENFASSUNG")
    print("=" * 80)
    
    for test_name, result in results.items():
        if test_name.endswith('_data'):
            continue
        print(f"{result} {test_name.replace('_', ' ').title()}")
    
    # Empfehlungen
    print("\n💡 EMPFEHLUNGEN:")
    print("-" * 50)
    
    if 'llm_data' in results:
        data = results['llm_data']
        if not data.get('UNTERNEHMEN'):
            print("❌ Unternehmen nicht extrahiert - LLM-Prompt verbessern")
        if not data.get('KONTAKTPERSON'):
            print("❌ Kontaktperson nicht extrahiert - Kontakt-Bereich-Erkennung verbessern")
        if not data.get('EMAIL'):
            print("❌ Email nicht extrahiert - Email-Pattern verbessern")
        if not data.get('TELEFON'):
            print("❌ Telefon nicht extrahiert - Telefon-Pattern verbessern")
    
    # Ergebnisse speichern
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"test_summary_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Test-Zusammenfassung gespeichert in: {output_file}")
    
    return results

if __name__ == "__main__":
    # Wechsle ins testing-Verzeichnis
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_all_tests()
