#!/usr/bin/env python3
"""Debug-Script für Job-Extraktion"""

from src.job_extractor import JobExtractor
import logging

# Logging einrichten
logging.basicConfig(level=logging.INFO)

def debug_extraction():
    """Debug-Funktion für Job-Extraktion"""
    try:
        extractor = JobExtractor()
        url = "https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op"
        
        # HTML-Inhalt laden
        html_content = extractor._fetch_webpage(url)
        print(f"HTML-Inhalt geladen: {len(html_content)} Zeichen")
        
        # Text extrahieren
        clean_text = extractor._extract_text_from_html(html_content)
        print(f"\nExtrahierter Text ({len(clean_text)} Zeichen):")
        print("="*60)
        print(clean_text[:2000])  # Erste 2000 Zeichen
        print("="*60)
        
        # Prüfe auf Kontaktinformationen
        if "Jan Schmitz-Elsen" in clean_text:
            print("✅ Kontaktperson 'Jan Schmitz-Elsen' gefunden!")
        else:
            print("❌ Kontaktperson 'Jan Schmitz-Elsen' NICHT gefunden!")
            
        if "Basel" in clean_text:
            print("✅ Arbeitsort 'Basel' gefunden!")
        else:
            print("❌ Arbeitsort 'Basel' NICHT gefunden!")
            
        if "Datalynx" in clean_text:
            print("✅ Unternehmen 'Datalynx' gefunden!")
        else:
            print("❌ Unternehmen 'Datalynx' NICHT gefunden!")
            
        # Strukturierte Extraktion
        job_info = extractor._extract_structured_info(clean_text, url)
        print(f"\nExtrahierte Informationen:")
        print(f"Unternehmen: {job_info.company}")
        print(f"Position: {job_info.position}")
        print(f"Adresse: {job_info.address}")
        print(f"Kontaktperson: {job_info.contact_person}")
        print(f"Titel: {job_info.contact_title}")
        print(f"Email: {job_info.email}")
        print(f"Telefon: {job_info.phone}")
        
    except Exception as e:
        print(f"Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_extraction()
