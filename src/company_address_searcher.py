import requests
import json
import logging
from typing import Optional, Dict, Any
from urllib.parse import quote
import time

class CompanyAddressSearcher:
    """
    Klasse für die automatische Suche von Firmendressen
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_company_address(self, company_name: str, location: Optional[str] = None) -> Optional[str]:
        """
        Sucht automatisch nach der Adresse eines Unternehmens
        
        Args:
            company_name: Name des Unternehmens
            location: Bekannter Standort (optional)
            
        Returns:
            str: Gefundene Adresse oder None
        """
        try:
            # Versuche verschiedene Suchmethoden
            address = self._search_via_google_maps(company_name, location)
            if address:
                return address
                
            address = self._search_via_web_scraping(company_name, location)
            if address:
                return address
                
            address = self._search_via_company_website(company_name, location)
            if address:
                return address
                
            return None
            
        except Exception as e:
            self.logger.error(f"Fehler bei Adressensuche für {company_name}: {e}")
            return None
    
    def _search_via_google_maps(self, company_name: str, location: Optional[str] = None) -> Optional[str]:
        """
        Sucht Adresse über Google Maps API (Nominatim als kostenlose Alternative)
        """
        try:
            # Verwende Nominatim (OpenStreetMap) als kostenlose Alternative
            search_query = company_name
            if location:
                search_query += f" {location}"
            search_query += " Schweiz"
            
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': search_query,
                'format': 'json',
                'addressdetails': 1,
                'limit': 1,
                'countrycodes': 'ch'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data and len(data) > 0:
                result = data[0]
                
                # Extrahiere Adressinformationen
                address_parts = []
                address_info = result.get('address', {})
                
                # Straße und Hausnummer
                if 'house_number' in address_info and 'road' in address_info:
                    address_parts.append(f"{address_info['road']} {address_info['house_number']}")
                elif 'road' in address_info:
                    address_parts.append(address_info['road'])
                
                # PLZ und Ort
                postcode = address_info.get('postcode', '')
                city = address_info.get('city') or address_info.get('town') or address_info.get('village')
                
                if postcode and city:
                    address_parts.append(f"{postcode} {city}")
                elif city:
                    address_parts.append(city)
                
                if address_parts:
                    full_address = ", ".join(address_parts)
                    self.logger.info(f"Adresse über Nominatim gefunden: {full_address}")
                    return full_address
                    
            time.sleep(1)  # Rate limiting
            return None
            
        except Exception as e:
            self.logger.error(f"Fehler bei Nominatim-Suche: {e}")
            return None
    
    def _search_via_web_scraping(self, company_name: str, location: Optional[str] = None) -> Optional[str]:
        """
        Sucht Adresse durch Web-Scraping von Suchmaschinen
        """
        try:
            # Suche nach Firmenname + "Adresse" + Standort
            search_query = f'"{company_name}" Adresse'
            if location:
                search_query += f' {location}'
            search_query += ' Schweiz'
            
            # Verwende DuckDuckGo als Suchmaschine (weniger Beschränkungen)
            url = "https://duckduckgo.com/html"
            params = {'q': search_query}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            # Einfache Textsuche nach Adressenmustern
            text = response.text
            
            # Suche nach Schweizer Adressenmustern (PLZ + Ort)
            import re
            
            # Pattern für Schweizer Adressen (4-stellige PLZ + Ort)
            address_patterns = [
                r'(\d{4}\s+[A-Za-zäöüÄÖÜ\s]+)',  # PLZ + Ort
                r'([A-Za-zäöüÄÖÜ\s]+\d+,?\s*\d{4}\s+[A-Za-zäöüÄÖÜ\s]+)',  # Straße + Hausnummer, PLZ + Ort
            ]
            
            for pattern in address_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    for match in matches:
                        # Filtere relevante Matches
                        if len(match) > 5 and any(city in match for city in ['Basel', 'Zürich', 'Bern', 'Luzern', 'Genf']):
                            self.logger.info(f"Adresse über Web-Scraping gefunden: {match}")
                            return match.strip()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Fehler bei Web-Scraping: {e}")
            return None
    
    def _search_via_company_website(self, company_name: str, location: Optional[str] = None) -> Optional[str]:
        """
        Sucht Adresse auf der Firmenwebsite
        """
        try:
            # Versuche häufige Domain-Endungen für Schweizer Firmen
            domain_endings = ['.ch', '.com', '.swiss']
            
            # Erzeuge mögliche Domain-Namen
            company_clean = company_name.lower().replace(' ', '').replace('-', '').replace('_', '')
            company_clean = ''.join(c for c in company_clean if c.isalnum())
            
            for ending in domain_endings:
                try:
                    url = f"https://www.{company_clean}{ending}"
                    response = self.session.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        # Suche nach Adresseninformationen auf der Website
                        text = response.text.lower()
                        
                        # Suche nach Kontakt/Impressum-Seiten
                        contact_keywords = ['kontakt', 'contact', 'impressum', 'imprint', 'standort', 'adresse']
                        
                        for keyword in contact_keywords:
                            if keyword in text:
                                # Hier könnte man spezifischere Extraktion implementieren
                                self.logger.info(f"Firmenwebsite gefunden: {url}")
                                # Vereinfachte Rückgabe für jetzt
                                return None
                                
                except:
                    continue
                    
            return None
            
        except Exception as e:
            self.logger.error(f"Fehler bei Website-Suche: {e}")
            return None
    
    def _extract_address_from_text(self, text: str) -> Optional[str]:
        """
        Extrahiert Adressinformationen aus Text
        """
        import re
        
        # Verschiedene Adressmuster für die Schweiz
        patterns = [
            # Vollständige Adresse: Straße Hausnummer, PLZ Ort
            r'([A-Za-zäöüÄÖÜ\s]+\d+,?\s*\d{4}\s+[A-Za-zäöüÄÖÜ\s]+)',
            # PLZ + Ort
            r'(\d{4}\s+[A-Za-zäöüÄÖÜ\s]+)',
            # Postfach-Adressen
            r'(Postfach\s+\d+,?\s*\d{4}\s+[A-Za-zäöüÄÖÜ\s]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].strip()
        
        return None
