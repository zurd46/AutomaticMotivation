#!/usr/bin/env python3
"""
Test Script für automatische Adressensuche
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.company_address_searcher import CompanyAddressSearcher
from src.recipient_controller import RecipientController
from src.models import JobDescription
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_address_search():
    """
    Testet die automatische Adressensuche für verschiedene Unternehmen
    """
    print("=== Test: Automatische Adressensuche ===")
    
    searcher = CompanyAddressSearcher()
    
    # Test-Unternehmen
    test_companies = [
        {"name": "Luzerner Kantonsspital", "location": "Luzern"},
        {"name": "UBS", "location": "Basel"},
        {"name": "Migros", "location": "Zürich"},
        {"name": "Roche", "location": "Basel"},
        {"name": "SwissLife", "location": "Zürich"},
    ]
    
    for company_info in test_companies:
        company = company_info["name"]
        location = company_info["location"]
        
        print(f"\n--- Suche für: {company} in {location} ---")
        
        try:
            address = searcher.search_company_address(company, location)
            if address:
                print(f"✅ Gefundene Adresse: {address}")
            else:
                print(f"❌ Keine Adresse gefunden")
                
        except Exception as e:
            print(f"❌ Fehler: {e}")

def test_recipient_controller_with_search():
    """
    Testet den RecipientController mit automatischer Adressensuche
    """
    print("\n=== Test: RecipientController mit automatischer Adressensuche ===")
    
    controller = RecipientController()
    
    # Test-Job ohne Adresse
    test_job = JobDescription(
        url="https://example.com/test-job",
        company="Luzerner Kantonsspital",
        position="ICT Supporter",
        location="Luzern",
        address="",  # Keine Adresse
        contact_person="",
        contact_title="",
        email="",
        phone="",
        description="Test-Job für Adressensuche",
        requirements="",
        benefits="",
        working_hours="",
        salary=""
    )
    
    print(f"Original Job-Daten:")
    print(f"  Unternehmen: '{test_job.company}'")
    print(f"  Standort: '{test_job.location}'")
    print(f"  Adresse: '{test_job.address}'")
    
    # Normalisiere Empfänger-Informationen
    normalized_job = controller.normalize_recipient_info(test_job)
    
    print(f"\nNach RecipientController (mit automatischer Suche):")
    print(f"  Empfänger-Unternehmen: '{normalized_job.company}'")
    print(f"  Empfänger-Standort: '{normalized_job.location}'") 
    print(f"  Empfänger-Adresse: '{normalized_job.address}'")

if __name__ == "__main__":
    test_address_search()
    test_recipient_controller_with_search()
