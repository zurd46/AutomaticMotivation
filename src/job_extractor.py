import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import json
from typing import Dict, List, Optional
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src.models import JobInfo, JobDescription
from config.config import Config

logger = logging.getLogger(__name__)

class JobExtractor:
    """Klasse zum Extrahieren von Job-Informationen aus URLs"""
    
    def __init__(self):
        self.config = Config.get_llm_config()
        self.llm = self._initialize_llm()
        self.logger = logging.getLogger(__name__)
        
    def _initialize_llm(self):
        """Initialisiert das LLM basierend auf der Konfiguration"""
        try:
            if self.config['provider'] == 'openrouter':
                llm = ChatOpenAI(
                    api_key=self.config['api_key'],
                    base_url=self.config['base_url'],
                    model=self.config['model'],
                    temperature=0.7,
                    max_tokens=2000
                )
            else:
                llm = ChatOpenAI(
                    api_key=self.config['api_key'],
                    model=self.config['model'],
                    temperature=self.config['temperature'],
                    max_tokens=2000
                )
            return llm
        except Exception as e:
            self.logger.error(f"Fehler bei LLM-Initialisierung: {e}")
            raise
        
    def extract_from_url(self, url: str) -> JobInfo:
        """
        Extrahiert Job-Informationen aus einer URL
        
        Args:
            url (str): URL der Stellenanzeige
            
        Returns:
            JobInfo: Extrahierte Job-Informationen
        """
        try:
            # Webseite laden
            html_content = self._fetch_webpage(url)
            
            # Text extrahieren
            clean_text = self._extract_text_from_html(html_content)
            
            # Mit LangChain strukturiert extrahieren
            job_info = self._extract_structured_info(clean_text, url)
            
            return job_info
            
        except Exception as e:
            self.logger.error(f"Fehler beim Extrahieren von URL {url}: {e}")
            raise
            
    def _fetch_webpage(self, url: str) -> str:
        """Lädt den HTML-Inhalt einer Webseite"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            return response.text
            
        except requests.RequestException as e:
            self.logger.error(f"Fehler beim Laden der Webseite {url}: {e}")
            raise
            
    def _extract_text_from_html(self, html_content: str) -> str:
        """Extrahiert bereinigten Text aus HTML und strukturierte Daten"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Zuerst nach strukturierten JSON-LD Daten suchen
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    if data.get('@type') == 'JobPosting':
                        # Strukturierte Daten gefunden - erstelle sauberen Text
                        structured_text = f"""
                        STELLENANZEIGE - STRUKTURIERTE DATEN:
                        
                        Titel: {data.get('title', '')}
                        Unternehmen: {data.get('hiringOrganization', {}).get('name', '')}
                        Standort: {data.get('jobLocation', {}).get('address', {}).get('addressLocality', '')}
                        Datum: {data.get('datePosted', '')}
                        
                        BESCHREIBUNG:
                        {data.get('description', '')}
                        
                        ZUSÄTZLICHE INFORMATIONEN:
                        Anstellungsart: {data.get('employmentType', '')}
                        Qualifikationen: {data.get('qualifications', '')}
                        """
                        
                        self.logger.info("JSON-LD JobPosting-Daten gefunden und verwendet")
                        return structured_text
                except Exception as e:
                    self.logger.debug(f"Fehler beim Parsen von JSON-LD: {e}")
                    continue
            
            # Erweiterte HTML-Extraktion mit Struktur-Erkennung
            extracted_sections = self._extract_structured_sections(soup)
            
            # Fallback: Überflüssige Tags entfernen
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()
            
            # Text extrahieren
            text = soup.get_text()
            
            # Text bereinigen
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Kombiniere strukturierte Sections mit dem normalen Text
            if extracted_sections:
                combined_text = f"""
                STRUKTURIERTE BEREICHE:
                {extracted_sections}
                
                VOLLSTÄNDIGER TEXT:
                {text}
                """
                return combined_text
            
            return text
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Textextraktion: {e}")
            raise
    
    def _extract_structured_sections(self, soup) -> str:
        """Extrahiert strukturierte Bereiche aus HTML"""
        try:
            sections = []
            
            # Suche nach typischen Job-Bereichen
            section_keywords = {
                'requirements': ['anforderungen', 'voraussetzungen', 'qualifikationen', 'sie bringen mit', 'ihr profil', 'requirements', 'qualifications'],
                'tasks': ['aufgaben', 'tätigkeiten', 'das erwartet sie', 'ihre aufgaben', 'responsibilities', 'tasks'],
                'benefits': ['wir bieten', 'benefits', 'vorteile', 'unser angebot', 'das bieten wir'],
                'company': ['über uns', 'unternehmen', 'about us', 'company', 'firma']
            }
            
            # Suche nach Überschriften und Listen
            for section_type, keywords in section_keywords.items():
                section_content = self._find_section_content(soup, keywords)
                if section_content:
                    sections.append(f"{section_type.upper()}:\n{section_content}")
            
            return '\n\n'.join(sections)
            
        except Exception as e:
            self.logger.debug(f"Fehler bei strukturierter Extraktion: {e}")
            return ""
    
    def _find_section_content(self, soup, keywords) -> str:
        """Findet Inhalte zu bestimmten Sektionen"""
        try:
            content_parts = []
            
            # Suche nach Überschriften mit Keywords
            for keyword in keywords:
                # Suche in verschiedenen Überschrift-Tags
                for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    headers = soup.find_all(tag, string=re.compile(keyword, re.IGNORECASE))
                    for header in headers:
                        # Sammle nachfolgenden Content
                        content = self._collect_following_content(header)
                        if content:
                            content_parts.append(content)
                
                # Suche in starken Texten und Spans
                for tag in ['strong', 'b', 'span', 'div']:
                    elements = soup.find_all(tag, string=re.compile(keyword, re.IGNORECASE))
                    for element in elements:
                        content = self._collect_following_content(element)
                        if content:
                            content_parts.append(content)
            
            return '\n'.join(content_parts)
            
        except Exception as e:
            self.logger.debug(f"Fehler bei Section-Content-Suche: {e}")
            return ""
    
    def _collect_following_content(self, element) -> str:
        """Sammelt nachfolgenden Content nach einem Element"""
        try:
            content_parts = []
            
            # Sammle Geschwister-Elemente
            for sibling in element.find_next_siblings():
                if sibling.name in ['ul', 'ol']:
                    # Listen sammeln
                    list_items = []
                    for li in sibling.find_all('li'):
                        list_items.append(f"- {li.get_text(strip=True)}")
                    if list_items:
                        content_parts.append('\n'.join(list_items))
                elif sibling.name in ['p', 'div']:
                    text = sibling.get_text(strip=True)
                    if text and len(text) > 20:  # Nur sinnvolle Texte
                        content_parts.append(text)
                elif sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    # Stoppe bei nächster Überschrift
                    break
                
                # Begrenze auf 3 Geschwister-Elemente
                if len(content_parts) >= 3:
                    break
            
            return '\n'.join(content_parts)
            
        except Exception as e:
            self.logger.debug(f"Fehler beim Sammeln von nachfolgendem Content: {e}")
            return ""
            
    def _extract_structured_info(self, text: str, url: str) -> JobInfo:
        """Extrahiert strukturierte Informationen mit LLM"""
        try:
            prompt = f"""
            Analysiere die folgende Stellenausschreibung und extrahiere die relevanten Informationen:

            TEXT:
            {text[:8000]}

            WICHTIGE HINWEISE FÜR DATALYNX JOBS:
            - Wenn es sich um eine Datalynx-Position handelt, verwende diese Informationen:
              * Unternehmen: Datalynx AG
              * Firmenadresse: Aeschenplatz 6, 4052 Basel, Schweiz
              * Kontaktperson: Jan Schmitz-Elsen
              * Titel: Team Lead Talent Acquisition
              * Email: jan.schmitz@datalynx.ch
              * Telefon: +41 79 425 10 45
            - Wenn der Arbeitsort "Basel" ist, verwende "Basel, Schweiz" als Adresse
            - Wenn "Datalynx AG" im Text erwähnt wird, verwende dies als Unternehmen

            BESONDERE AUFMERKSAMKEIT FÜR ANFORDERUNGEN:
            - Suche nach Abschnitten wie "Anforderungen", "Voraussetzungen", "Qualifikationen", "Sie bringen mit", "Requirements", "Ihr Profil"
            - Suche nach Aufgaben/Tätigkeiten wie "Ihre Aufgaben", "Das erwartet Sie", "Responsibilities", "Tätigkeiten"
            - Identifiziere ob es sich um IT-Support, Entwicklung, oder andere IT-Bereiche handelt
            - Extrahiere technische Kenntnisse, Soft Skills, Ausbildung und Erfahrung separat

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
            BESCHREIBUNG: [Kurze Beschreibung der Position und Hauptaufgaben]
            ANFORDERUNGEN: [Alle wichtigen Anforderungen, Qualifikationen und Voraussetzungen in einem zusammenhängenden Text]
            BENEFITS: [Angebotene Leistungen]
            ARBEITSZEIT: [Arbeitszeiten, falls genannt]
            GEHALT: [Gehaltsangaben, falls genannt]
            
            WICHTIGE HINWEISE: 
            - Suche im gesamten Text nach "Kontakt", "Ansprechpartner", "Contact" Abschnitten
            - Nutze die oben genannten Datalynx-Kontaktdaten wenn es eine Datalynx-Position ist
            - Wenn keine spezifische Kontaktperson gefunden wird, schreibe "Nicht angegeben"
            - Bei Arbeitsort "Basel" verwende "Basel, Schweiz" als Adresse
            - Für ANFORDERUNGEN: Fasse alle relevanten Qualifikationen, Kenntnisse und Erfahrungen zusammen
            """
            
            messages = [
                SystemMessage(content="Du bist ein Experte für die Extraktion von Stelleninformationen. Analysiere Stellenausschreibungen präzise und strukturiert."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            extracted_info = self._parse_llm_response(response.content)
            
            # JobInfo-Objekt erstellen
            job_info = JobInfo(
                url=url,
                company=extracted_info.get('UNTERNEHMEN', 'Nicht angegeben') or 'Nicht angegeben',
                position=extracted_info.get('POSITION', 'Nicht angegeben') or 'Nicht angegeben',
                department=extracted_info.get('BEREICH') or None,
                location=extracted_info.get('STANDORT', 'Nicht angegeben') or 'Nicht angegeben',
                address=extracted_info.get('ADRESSE', 'Nicht angegeben') or 'Nicht angegeben',
                contact_person=extracted_info.get('KONTAKTPERSON') or None,
                contact_title=extracted_info.get('KONTAKT_TITEL') or None,
                email=extracted_info.get('EMAIL') or None,
                phone=extracted_info.get('TELEFON') or None,
                description=extracted_info.get('BESCHREIBUNG', 'Nicht angegeben') or 'Nicht angegeben',
                requirements=extracted_info.get('ANFORDERUNGEN', 'Nicht angegeben') or 'Nicht angegeben',
                benefits=extracted_info.get('BENEFITS') or None,
                working_hours=extracted_info.get('ARBEITSZEIT') or None,
                salary=extracted_info.get('GEHALT') or None
            )
            
            self.logger.info(f"Job-Informationen erfolgreich extrahiert: {job_info.company} - {job_info.position}")
            return job_info
            
        except Exception as e:
            self.logger.error(f"Fehler bei der strukturierten Extraktion: {e}")
            # Fallback-JobInfo erstellen
            return JobInfo(
                url=url,
                company="Nicht extrahiert",
                position="Nicht extrahiert",
                address="Nicht extrahiert",
                location="Nicht extrahiert",
                description="Fehler bei der Extraktion",
                requirements="Fehler bei der Extraktion"
            )
            
    def _parse_llm_response(self, response: str) -> Dict[str, str]:
        """Parst die LLM-Antwort in ein Dictionary"""
        try:
            info = {}
            lines = response.split('\n')
            current_key = None
            current_value = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Prüfe ob die Zeile ein neues Feld beginnt
                if ':' in line and any(key in line.upper() for key in ['UNTERNEHMEN', 'POSITION', 'BEREICH', 'STANDORT', 'ADRESSE', 'KONTAKTPERSON', 'KONTAKT_TITEL', 'EMAIL', 'TELEFON', 'BESCHREIBUNG', 'ANFORDERUNGEN', 'BENEFITS', 'ARBEITSZEIT', 'GEHALT']):
                    # Speichere das vorherige Feld
                    if current_key and current_value:
                        value = ' '.join(current_value).strip()
                        if value and value != "Nicht angegeben":
                            info[current_key] = value
                        else:
                            info[current_key] = None
                    
                    # Starte neues Feld
                    key, value = line.split(':', 1)
                    current_key = key.strip()
                    current_value = [value.strip()] if value.strip() else []
                else:
                    # Füge zur aktuellen Beschreibung hinzu
                    if current_key and line:
                        current_value.append(line)
            
            # Speichere das letzte Feld
            if current_key and current_value:
                value = ' '.join(current_value).strip()
                if value and value != "Nicht angegeben":
                    info[current_key] = value
                else:
                    info[current_key] = None
                        
            return info
            
        except Exception as e:
            self.logger.error(f"Fehler beim Parsen der LLM-Antwort: {e}")
            self.logger.debug(f"Response content: {response}")
            return {}
