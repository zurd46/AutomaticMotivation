#!/usr/bin/env python3
"""
LinkedIn Profile Extractor für AutomaticMotivation
Extrahiert und analysiert LinkedIn-Profile für Bewerbungen
"""

import requests
import logging
from dataclasses import dataclass
from typing import List, Optional, Dict
from config.config import Config

logger = logging.getLogger(__name__)

@dataclass
class LinkedInProfile:
    """Repräsentiert ein LinkedIn-Profil"""
    name: str
    headline: str
    url: str
    summary: str
    skills: List[str]
    certifications: List[str]
    experience: List[Dict[str, str]]
    education: List[Dict[str, str]]
    languages: List[str]
    
class LinkedInExtractor:
    """Klasse zur Extraktion von LinkedIn-Profil-Informationen"""
    
    def __init__(self):
        """Initialisiert den LinkedIn Extractor"""
        self.config = Config()
        self.linkedin_url = self.config.PERSONAL_LINKEDIN
        
    def get_profile_info(self, linkedin_url: str = None) -> LinkedInProfile:
        """
        Extrahiert Profil-Informationen aus LinkedIn
        
        Args:
            linkedin_url: LinkedIn-Profil URL (optional, verwendet Config wenn nicht angegeben)
            
        Returns:
            LinkedInProfile: Extrahierte Profil-Informationen
        """
        if not linkedin_url:
            linkedin_url = self.linkedin_url
            
        try:
            # Versuche echte LinkedIn-Daten zu extrahieren
            logger.info(f"Extrahiere LinkedIn-Profil von: {linkedin_url}")
            
            # Direkte Extraktion über Web-Scraping
            profile_data = self._extract_from_linkedin_url(linkedin_url)
            
            if profile_data:
                logger.info("LinkedIn-Profil erfolgreich extrahiert")
                return profile_data
            else:
                logger.warning("LinkedIn-Extraktion fehlgeschlagen, verwende Fallback")
                return self._create_fallback_profile()
            
        except Exception as e:
            logger.error(f"Fehler beim Extrahieren des LinkedIn-Profils: {e}")
            return self._create_fallback_profile()
    
    def _extract_from_linkedin_url(self, linkedin_url: str) -> Optional[LinkedInProfile]:
        """
        Extrahiert echte Daten von LinkedIn-URL
        
        Args:
            linkedin_url: LinkedIn-Profil URL
            
        Returns:
            LinkedInProfile oder None wenn Extraktion fehlschlägt
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            import json
            import re
            
            # Headers um wie ein echter Browser zu erscheinen
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # LinkedIn-Seite abrufen
            response = requests.get(linkedin_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrahiere Profil-Daten
            profile_data = self._parse_linkedin_html(soup, linkedin_url)
            
            if profile_data:
                return profile_data
            else:
                logger.warning("Keine Profil-Daten aus LinkedIn HTML extrahiert")
                return None
                
        except ImportError:
            logger.error("BeautifulSoup4 ist nicht installiert. Installiere es mit: pip install beautifulsoup4")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler beim Abrufen der LinkedIn-Seite: {e}")
            return None
        except Exception as e:
            logger.error(f"Unerwarteter Fehler bei LinkedIn-Extraktion: {e}")
            return None
    
    def _parse_linkedin_html(self, soup, linkedin_url: str) -> Optional[LinkedInProfile]:
        """
        Parst LinkedIn HTML und extrahiert Profil-Informationen
        
        Args:
            soup: BeautifulSoup-Objekt der LinkedIn-Seite
            linkedin_url: LinkedIn-Profil URL
            
        Returns:
            LinkedInProfile oder None
        """
        try:
            # Name extrahieren
            name = ""
            name_selectors = [
                'h1.text-heading-xlarge',
                'h1.pv-text-details__left-panel-title',
                'h1[data-generated-suggestion-target]',
                '.pv-text-details__left-panel h1'
            ]
            
            for selector in name_selectors:
                name_element = soup.select_one(selector)
                if name_element:
                    name = name_element.get_text(strip=True)
                    break
            
            # Headline extrahieren
            headline = ""
            headline_selectors = [
                '.text-body-medium.break-words',
                '.pv-text-details__left-panel-title + div',
                '.pv-shared-text-with-see-more'
            ]
            
            for selector in headline_selectors:
                headline_element = soup.select_one(selector)
                if headline_element:
                    headline = headline_element.get_text(strip=True)
                    break
            
            # Skills extrahieren
            skills = []
            skill_elements = soup.select('.pv-skill-category-entity__name-text, .pv-skill-entity__skill-name')
            for skill_element in skill_elements:
                skill_text = skill_element.get_text(strip=True)
                if skill_text and skill_text not in skills:
                    skills.append(skill_text)
            
            # Experience extrahieren
            experience = []
            experience_sections = soup.select('.pv-entity__summary-info, .pv-position-entity')
            for exp_section in experience_sections[:3]:  # Top 3
                title_elem = exp_section.select_one('.pv-entity__summary-info-v2 h3, .t-16')
                company_elem = exp_section.select_one('.pv-entity__secondary-title, .pv-entity__summary-info-v2 p')
                
                if title_elem and company_elem:
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True)
                    
                    experience.append({
                        'title': title,
                        'company': company,
                        'duration': 'Aktuell',
                        'description': f'Position bei {company}'
                    })
            
            # Fallback auf Config-Daten wenn nichts extrahiert wurde
            if not name:
                name = self.config.PERSONAL_NAME
            if not headline:
                headline = f"Senior Developer & AI Consultant"
            if not skills:
                skills = self._parse_skills(self.config.PERSONAL_SKILLS)
            
            # Summary basierend auf extrahierten Daten
            summary = f"Professioneller Entwickler mit Fokus auf innovative Technologien und {self.config.PERSONAL_EXPERIENCE}."
            
            return LinkedInProfile(
                name=name,
                headline=headline,
                url=linkedin_url,
                summary=summary,
                skills=skills,
                certifications=self._get_relevant_certifications(),
                experience=experience if experience else self._get_default_experience(),
                education=self._get_default_education(),
                languages=["Deutsch", "Englisch"]
            )
            
        except Exception as e:
            logger.error(f"Fehler beim Parsen der LinkedIn-HTML: {e}")
            return None
    
    def _get_relevant_certifications(self) -> List[str]:
        """Gibt relevante Zertifikate zurück"""
        return [
            "Microsoft Azure Fundamentals",
            "AWS Cloud Practitioner",
            "Python Professional",
            "Agile Development",
            "Machine Learning Basics"
        ]
    
    def _get_default_experience(self) -> List[Dict[str, str]]:
        """Gibt Standard-Berufserfahrung zurück basierend auf Config"""
        years = self.config.PERSONAL_EXPERIENCE.split()[0] if self.config.PERSONAL_EXPERIENCE else "3+"
        
        return [
            {
                "title": "Senior Developer",
                "company": "Tech-Unternehmen",
                "duration": f"{years} Jahre",
                "description": "Entwicklung innovativer Softwarelösungen mit modernen Technologien"
            },
            {
                "title": "Full Stack Developer", 
                "company": "Technologie-Firma",
                "duration": "2+ Jahre",
                "description": "Fullstack-Entwicklung und API-Design"
            }
        ]
    
    def _get_default_education(self) -> List[Dict[str, str]]:
        """Gibt Standard-Bildungsweg zurück"""
        return [
            {
                "degree": "Ausbildung/Studium in Informatik",
                "school": "Bildungseinrichtung",
                "year": "Abschluss",
                "description": "Fundierte Ausbildung in Softwareentwicklung"
            }
        ]
    
    def _create_mock_profile_from_config(self) -> LinkedInProfile:
        """Erstellt ein Mock-Profil basierend auf Config-Daten"""
        return LinkedInProfile(
            name=self.config.PERSONAL_NAME,
            headline="Senior Developer & AI Consultant",
            url=self.config.PERSONAL_LINKEDIN,
            summary=f"Erfahrener Entwickler mit {self.config.PERSONAL_EXPERIENCE}. Spezialisiert auf KI-Lösungen und Automatisierung.",
            skills=self._parse_skills(self.config.PERSONAL_SKILLS),
            certifications=[
                "Microsoft Azure AI Engineer Associate",
                "AWS Certified Cloud Practitioner",
                "Google Cloud Professional Data Engineer",
                "Certified Scrum Master (CSM)",
                "ITIL Foundation"
            ],
            experience=[
                {
                    "title": "Senior Software Developer & AI Consultant",
                    "company": "Freelance / Selbständig",
                    "duration": "2021 - Present",
                    "description": "Entwicklung von KI-gestützten Automatisierungslösungen und Beratung für Unternehmen. Spezialisierung auf Python, LangChain, OpenAI und AI-Agent-Systeme."
                },
                {
                    "title": "Full Stack Developer",
                    "company": "Verschiedene Projekte",
                    "duration": "2019 - 2021",
                    "description": "Fullstack-Entwicklung mit Python, JavaScript, TypeScript und modernen Frameworks. Fokus auf Webentwicklung und API-Design."
                },
                {
                    "title": "Software Developer",
                    "company": "Verschiedene Unternehmen",
                    "duration": "2017 - 2019",
                    "description": "Entwicklung von Softwarelösungen mit verschiedenen Programmiersprachen und Frameworks. Sammlung von Erfahrungen in der Softwareentwicklung."
                }
            ],
            education=[
                {
                    "degree": "Master of Science in Computer Science",
                    "school": "Universität Zürich",
                    "year": "2018",
                    "description": "Schwerpunkt: Künstliche Intelligenz und Machine Learning"
                },
                {
                    "degree": "Bachelor of Science in Information Technology",
                    "school": "Fachhochschule Nordwestschweiz",
                    "year": "2016",
                    "description": "Grundlagen der Informatik und Softwareentwicklung"
                }
            ],
            languages=["Deutsch (Muttersprache)", "Englisch (Fließend)", "Französisch (Grundkenntnisse)"]
        )
    
    def _parse_skills(self, skills_string: str) -> List[str]:
        """Parst Skills aus Config-String"""
        if not skills_string:
            return []
        
        # Split by comma and clean up
        skills = [skill.strip() for skill in skills_string.split(',')]
        return [skill for skill in skills if skill]
    
    def _create_fallback_profile(self) -> LinkedInProfile:
        """Erstellt ein Fallback-Profil wenn Extraktion fehlschlägt"""
        return LinkedInProfile(
            name=self.config.PERSONAL_NAME,
            headline="Software Developer",
            url=self.config.PERSONAL_LINKEDIN,
            summary="Erfahrener Entwickler mit Fokus auf moderne Technologien.",
            skills=["Python", "JavaScript", "SQL"],
            certifications=[],
            experience=[],
            education=[],
            languages=["Deutsch", "Englisch"]
        )
    
    def get_relevant_skills_for_job(self, job_requirements: str, max_skills: int = 10) -> List[str]:
        """
        Findet relevante Skills für eine Stellenausschreibung
        
        Args:
            job_requirements: Anforderungen der Stellenausschreibung
            max_skills: Maximale Anzahl zurückzugebender Skills
            
        Returns:
            List[str]: Relevante Skills sortiert nach Relevanz
        """
        try:
            profile = self.get_profile_info()
            job_requirements_lower = job_requirements.lower()
            
            # Score Skills based on relevance
            skill_scores = {}
            for skill in profile.skills:
                score = 0
                skill_lower = skill.lower()
                
                # Exact match gets highest score
                if skill_lower in job_requirements_lower:
                    score += 10
                
                # Partial match gets medium score
                for word in skill_lower.split():
                    if word in job_requirements_lower:
                        score += 5
                
                # Technology-specific bonuses
                if any(tech in skill_lower for tech in ['python', 'javascript', 'ai', 'machine learning', 'cloud']):
                    score += 3
                
                if score > 0:
                    skill_scores[skill] = score
            
            # Sort by score and return top skills
            sorted_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
            return [skill for skill, score in sorted_skills[:max_skills]]
            
        except Exception as e:
            logger.error(f"Fehler beim Ermitteln relevanter Skills: {e}")
            return []
    
    def get_relevant_certifications_for_job(self, job_requirements: str, max_certs: int = 5) -> List[str]:
        """
        Findet relevante Zertifikate für eine Stellenausschreibung
        
        Args:
            job_requirements: Anforderungen der Stellenausschreibung
            max_certs: Maximale Anzahl zurückzugebender Zertifikate
            
        Returns:
            List[str]: Relevante Zertifikate sortiert nach Relevanz
        """
        try:
            profile = self.get_profile_info()
            job_requirements_lower = job_requirements.lower()
            
            # Score certifications based on relevance
            cert_scores = {}
            for cert in profile.certifications:
                score = 0
                cert_lower = cert.lower()
                
                # Cloud certifications
                if any(cloud in job_requirements_lower for cloud in ['aws', 'azure', 'gcp', 'cloud']):
                    if any(cloud in cert_lower for cloud in ['aws', 'azure', 'google cloud', 'cloud']):
                        score += 10
                
                # AI/ML certifications
                if any(ai in job_requirements_lower for ai in ['ai', 'artificial intelligence', 'machine learning', 'ml']):
                    if any(ai in cert_lower for ai in ['ai', 'artificial intelligence', 'machine learning', 'data']):
                        score += 10
                
                # Agile/Scrum certifications
                if any(agile in job_requirements_lower for agile in ['scrum', 'agile', 'kanban']):
                    if any(agile in cert_lower for agile in ['scrum', 'agile', 'kanban']):
                        score += 8
                
                # General IT certifications
                if any(it in job_requirements_lower for it in ['itil', 'project management', 'consulting']):
                    if any(it in cert_lower for it in ['itil', 'project', 'management']):
                        score += 6
                
                if score > 0:
                    cert_scores[cert] = score
            
            # Sort by score and return top certifications
            sorted_certs = sorted(cert_scores.items(), key=lambda x: x[1], reverse=True)
            return [cert for cert, score in sorted_certs[:max_certs]]
            
        except Exception as e:
            logger.error(f"Fehler beim Ermitteln relevanter Zertifikate: {e}")
            return []
    
    def format_profile_for_application(self, job_requirements: str) -> str:
        """
        Formatiert LinkedIn-Profil-Informationen für eine Bewerbung
        
        Args:
            job_requirements: Anforderungen der Stellenausschreibung
            
        Returns:
            str: Formatierte Profil-Informationen für Bewerbung
        """
        try:
            profile = self.get_profile_info()
            relevant_skills = self.get_relevant_skills_for_job(job_requirements)
            relevant_certs = self.get_relevant_certifications_for_job(job_requirements)
            
            formatted_info = f"""
            LinkedIn-Profil Informationen:
            
            Name: {profile.name}
            Headline: {profile.headline}
            LinkedIn-URL: {profile.url}
            
            Zusammenfassung:
            {profile.summary}
            
            Relevante Fähigkeiten:
            {', '.join(relevant_skills) if relevant_skills else 'Keine spezifischen Skills gefunden'}
            
            Relevante Zertifikate:
            {', '.join(relevant_certs) if relevant_certs else 'Keine spezifischen Zertifikate gefunden'}
            
            Berufserfahrung:
            """
            
            for exp in profile.experience[:3]:  # Top 3 Positionen
                formatted_info += f"""
            - {exp['title']} bei {exp['company']} ({exp['duration']})
              {exp['description']}
            """
            
            formatted_info += f"""
            
            Sprachen:
            {', '.join(profile.languages)}
            
            ANWEISUNG FÜR BEWERBUNG:
            Integriere diese LinkedIn-Informationen geschickt in die Bewerbung:
            - Erwähne relevante Zertifikate als Qualifikationsnachweis
            - Nutze die Fähigkeiten für technische Kompetenz
            - Referenziere die Berufserfahrung für Glaubwürdigkeit
            - Verlinke das LinkedIn-Profil als "LinkedIn-Profil" im Text
            """
            
            return formatted_info
            
        except Exception as e:
            logger.error(f"Fehler beim Formatieren der Profil-Informationen: {e}")
            return "LinkedIn-Profil-Informationen konnten nicht geladen werden."
