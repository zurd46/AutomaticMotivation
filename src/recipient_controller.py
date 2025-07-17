#!/usr/bin/env python3
"""
Recipient Information Controller
Kontrolliert und standardisiert Empfänger-Informationen für Motivationsschreiben
"""

import os
import sys
import re
from typing import Dict, Optional, Tuple

# Füge src-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import JobDescription
from src.company_address_searcher import CompanyAddressSearcher
import logging

logger = logging.getLogger(__name__)

class RecipientController:
    """
    Kontrolliert und standardisiert Empfänger-Informationen für Motivationsschreiben
    """
    
    def __init__(self):
        self.logger = logger
        self.address_searcher = CompanyAddressSearcher()
    
    def normalize_recipient_info(self, job_description: JobDescription) -> JobDescription:
        """
        Normalisiert Empfänger-Informationen basierend auf verfügbaren Daten
        
        Args:
            job_description: Ursprüngliche Job-Beschreibung
            
        Returns:
            JobDescription: Normalisierte Job-Beschreibung mit korrekten Empfänger-Daten
        """
        # Erstelle eine Kopie der Job-Beschreibung
        normalized_job = JobDescription(
            position=job_description.position,
            company=job_description.company,
            contact_person=job_description.contact_person,
            description=job_description.description,
            requirements=job_description.requirements,
            benefits=job_description.benefits,
            location=job_description.location,
            address=job_description.address,
            department=job_description.department,
            url=job_description.url,
            working_hours=job_description.working_hours
        )
        
        # Prüfe und normalisiere Kontaktperson
        normalized_job.contact_person = self._normalize_contact_person(
            job_description.contact_person,
            job_description.company
        )
        
        # Prüfe und normalisiere Firmenadresse
        normalized_job.address = self._normalize_company_address(
            job_description.address,
            job_description.company,
            job_description.location
        )
        
        self.logger.info(f"Empfänger-Informationen normalisiert: {normalized_job.contact_person} @ {normalized_job.company}")
        
        return normalized_job
    
    def _normalize_contact_person(self, contact_person: Optional[str], company: str) -> str:
        """
        Normalisiert Kontaktperson-Informationen
        
        Args:
            contact_person: Ursprüngliche Kontaktperson
            company: Firmenname
            
        Returns:
            str: Normalisierte Kontaktperson
        """
        # Definiere "leere" Werte
        empty_values = [None, "", "Nicht angegeben", "nicht angegeben", "N/A", "n/a"]
        
        if contact_person in empty_values:
            self.logger.info(f"Keine Kontaktperson gefunden, verwende Firmenname: {company}")
            return company
        
        # Bereinige Kontaktperson
        cleaned_contact = contact_person.strip()
        
        # Prüfe, ob Kontaktperson gleich Firmenname ist (redundant)
        if cleaned_contact.lower() == company.lower():
            self.logger.info(f"Kontaktperson ist gleich Firmenname, verwende Firmenname: {company}")
            return company
        
        # Prüfe, ob Kontaktperson zu generisch ist
        generic_contacts = [
            "hr", "human resources", "personalabteilung", "recruiting", "bewerbung",
            "bewerbungen", "karriere", "jobs", "stellenangebote", "info", "kontakt",
            "hr team", "human resources team", "personalteam", "recruiting team"
        ]
        
        if cleaned_contact.lower() in generic_contacts:
            self.logger.info(f"Generische Kontaktperson gefunden ({cleaned_contact}), verwende Firmenname: {company}")
            return company
        
        self.logger.info(f"Spezifische Kontaktperson gefunden: {cleaned_contact}")
        return cleaned_contact
    
    def _normalize_company_address(self, address: Optional[str], company: str, location: Optional[str]) -> str:
        """
        Normalisiert Firmenadresse
        
        Args:
            address: Ursprüngliche Adresse
            company: Firmenname
            location: Standort
            
        Returns:
            str: Normalisierte Firmenadresse
        """
        # Definiere "leere" Werte
        empty_values = [None, "", "Nicht angegeben", "nicht angegeben", "N/A", "n/a"]
        
        if address in empty_values:
            self.logger.info(f"Keine Firmenadresse gefunden, suche automatisch für: {company}")
            
            # Versuche automatische Adressensuche
            searched_address = self.address_searcher.search_company_address(company, location)
            if searched_address:
                self.logger.info(f"Automatisch gefundene Adresse: {searched_address}")
                return self._format_address_lines(searched_address, company)
            else:
                self.logger.warning(f"Automatische Adressensuche fehlgeschlagen für: {company}")
                return self._create_standard_address(company, location)
        
        # Bereinige Adresse
        cleaned_address = address.strip()
        
        # Prüfe, ob Adresse zu kurz oder unvollständig ist
        if len(cleaned_address) < 10:
            self.logger.info(f"Adresse zu kurz ({cleaned_address}), suche automatisch für: {company}")
            
            # Versuche automatische Adressensuche
            searched_address = self.address_searcher.search_company_address(company, location)
            if searched_address:
                self.logger.info(f"Automatisch gefundene Adresse: {searched_address}")
                return self._format_address_lines(searched_address, company)
            else:
                self.logger.warning(f"Automatische Adressensuche fehlgeschlagen für: {company}")
                return self._create_standard_address(company, location)
        
        # Formatiere Adresse in Zeilen
        formatted_address = self._format_address_lines(cleaned_address, company)
        
        # Entferne Zeilenumbrüche für bessere Kompatibilität
        formatted_address = formatted_address.replace('\n', ', ')
        
        self.logger.info(f"Adresse formatiert: {formatted_address}")
        return formatted_address
    
    def _create_standard_address(self, company: str, location: Optional[str]) -> str:
        """
        Erstellt Standard-Adresse basierend auf Firmenname und Standort
        
        Args:
            company: Firmenname
            location: Standort (optional)
            
        Returns:
            str: Standard-Adresse (ohne Firmennamen, da dieser separat angezeigt wird)
        """
        address_lines = []
        
        if location and location not in ["Nicht angegeben", "nicht angegeben", ""]:
            # Nur Standort verwenden, Firmenname wird separat angezeigt
            address_lines.append(location)
        else:
            # Fallback: Platzhalter für Adresse
            address_lines.append("Adresse nicht verfügbar")
        
        # Komma-getrennte Adresse für bessere Kompatibilität
        return ", ".join(address_lines)
    
    def _format_address_lines(self, address: str, company: str) -> str:
        """
        Formatiert Adresse in korrekte Zeilen
        
        Args:
            address: Rohadresse
            company: Firmenname
            
        Returns:
            str: Formatierte Adresse
        """
        # Entferne Firmenname aus Adresse, falls enthalten
        address_without_company = address
        if company.lower() in address.lower():
            address_without_company = re.sub(re.escape(company), "", address, flags=re.IGNORECASE).strip()
            # Entferne führende Kommas oder Bindestriche
            address_without_company = re.sub(r'^[,\-\s]+', '', address_without_company)
        
        # Teile Adresse in Komponenten
        if ',' in address_without_company:
            # Komma-getrennte Adresse
            parts = [part.strip() for part in address_without_company.split(',') if part.strip()]
        else:
            # Adresse ohne Kommas
            parts = [address_without_company.strip()]
        
        # Baue formatierte Adresse auf (ohne Firmennamen, da dieser separat angezeigt wird)
        formatted_lines = []
        
        for part in parts:
            if part and part.lower() != company.lower():  # Vermeide Duplikate des Firmennamens
                formatted_lines.append(part)
        
        # Komma-getrennte Adresse für bessere Kompatibilität
        return ", ".join(formatted_lines)
    
    def validate_recipient_info(self, job_description: JobDescription) -> Dict[str, any]:
        """
        Validiert Empfänger-Informationen und gibt Analyse zurück
        
        Args:
            job_description: Job-Beschreibung
            
        Returns:
            Dict: Validierungsergebnis
        """
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        
        # Prüfe Kontaktperson
        if not job_description.contact_person or job_description.contact_person in ["Nicht angegeben", ""]:
            validation_result["warnings"].append("Keine spezifische Kontaktperson gefunden")
            validation_result["recommendations"].append("Verwende Firmenname als Kontaktperson")
        elif job_description.contact_person.lower() == job_description.company.lower():
            validation_result["warnings"].append("Kontaktperson ist gleich Firmenname")
        
        # Prüfe Firmenadresse
        if not job_description.address or job_description.address in ["Nicht angegeben", ""]:
            validation_result["warnings"].append("Keine Firmenadresse gefunden")
            validation_result["recommendations"].append("Verwende Standard-Adresse mit Firmenname")
        elif len(job_description.address) < 10:
            validation_result["warnings"].append("Firmenadresse scheint unvollständig")
        
        # Prüfe Firmenname
        if not job_description.company or job_description.company in ["Nicht angegeben", ""]:
            validation_result["errors"].append("Firmenname fehlt")
            validation_result["valid"] = False
        
        return validation_result

def test_recipient_controller():
    """Test-Funktion für RecipientController"""
    print("=== Test: RecipientController ===\n")
    
    controller = RecipientController()
    
    # Test 1: Keine Kontaktperson
    print("Test 1: Keine Kontaktperson")
    job1 = JobDescription(
        position="Software Engineer",
        company="Tech AG",
        contact_person=None,
        description="Test Job",
        requirements="Programming skills",
        benefits="Good salary",
        location="Zürich",
        address="Tech AG, Techstrasse 1, 8001 Zürich",
        department="IT",
        url="https://example.com",
        working_hours="100%"
    )
    
    normalized1 = controller.normalize_recipient_info(job1)
    validation1 = controller.validate_recipient_info(job1)
    
    print(f"Original Kontaktperson: {job1.contact_person}")
    print(f"Normalisierte Kontaktperson: {normalized1.contact_person}")
    print(f"Validierung: {validation1}")
    print()
    
    # Test 2: Kontaktperson gleich Firmenname
    print("Test 2: Kontaktperson gleich Firmenname")
    job2 = JobDescription(
        position="Data Scientist",
        company="Data Corp",
        contact_person="Data Corp",
        description="Test Job",
        requirements="Data skills",
        benefits="Benefits",
        location="Basel",
        address="Data Corp, Datenweg 5, 4000 Basel",
        department="Analytics",
        url="https://example.com",
        working_hours="80%"
    )
    
    normalized2 = controller.normalize_recipient_info(job2)
    validation2 = controller.validate_recipient_info(job2)
    
    print(f"Original Kontaktperson: {job2.contact_person}")
    print(f"Normalisierte Kontaktperson: {normalized2.contact_person}")
    print(f"Validierung: {validation2}")
    print()
    
    # Test 3: Spezifische Kontaktperson
    print("Test 3: Spezifische Kontaktperson")
    job3 = JobDescription(
        position="ICT Support",
        company="Luzerner Kantonsspital",
        contact_person="Jan Enz",
        description="Test Job",
        requirements="IT Support",
        benefits="Hospital benefits",
        location="Luzern",
        address="Luzerner Kantonsspital, Spitalstrasse 1, 6000 Luzern",
        department="IT",
        url="https://example.com",
        working_hours="100%"
    )
    
    normalized3 = controller.normalize_recipient_info(job3)
    validation3 = controller.validate_recipient_info(job3)
    
    print(f"Original Kontaktperson: {job3.contact_person}")
    print(f"Normalisierte Kontaktperson: {normalized3.contact_person}")
    print(f"Validierung: {validation3}")
    print()
    
    # Test 4: Keine Adresse
    print("Test 4: Keine Adresse")
    job4 = JobDescription(
        position="Developer",
        company="StartupXYZ",
        contact_person="HR Team",
        description="Test Job",
        requirements="Dev skills",
        benefits="Startup benefits",
        location="Bern",
        address="",  # Leere Adresse statt None
        department="Development",
        url="https://example.com",
        working_hours="100%"
    )
    
    normalized4 = controller.normalize_recipient_info(job4)
    validation4 = controller.validate_recipient_info(job4)
    
    print(f"Original Adresse: {job4.address}")
    print(f"Normalisierte Adresse: {normalized4.address}")
    print(f"Validierung: {validation4}")
    print()

if __name__ == "__main__":
    test_recipient_controller()
