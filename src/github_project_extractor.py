#!/usr/bin/env python3
"""
GitHub Project Extractor für AutomaticMotivation
Ruft relevante Projekte von GitHub ab und wählt passende für Bewerbungen aus
"""

import requests
import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config.config import Config
import logging

logger = logging.getLogger(__name__)

@dataclass
class GitHubProject:
    """Repräsentiert ein GitHub-Projekt"""
    name: str
    description: str
    url: str
    language: str
    topics: List[str]
    stars: int
    is_fork: bool
    
class GitHubProjectExtractor:
    """Klasse zum Extrahieren relevanter GitHub-Projekte"""
    
    def __init__(self):
        self.config = Config.get_llm_config()
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self):
        """Initialisiert das LLM für die Projekt-Auswahl"""
        try:
            if self.config['provider'] == 'openrouter':
                llm = ChatOpenAI(
                    api_key=self.config['api_key'],
                    base_url=self.config['base_url'],
                    model=self.config['model'],
                    temperature=0.3,  # Niedrigere Temperatur für konsistente Auswahl
                    max_tokens=1000
                )
            else:
                llm = ChatOpenAI(
                    api_key=self.config['api_key'],
                    model=self.config['model'],
                    temperature=0.3,
                    max_tokens=1000
                )
            return llm
        except Exception as e:
            logger.error(f"Fehler bei LLM-Initialisierung: {e}")
            raise
    
    def get_github_projects(self, github_url: str) -> List[GitHubProject]:
        """
        Ruft alle öffentlichen Repositories von GitHub ab mit Caching
        
        Args:
            github_url: GitHub-Profil URL (z.B. https://github.com/username)
            
        Returns:
            List von GitHubProject-Objekten
        """
        try:
            # Extrahiere Username aus URL
            username = github_url.split('/')[-1]
            
            # Nutze Config-Cache für Projekt-URLs
            project_urls = Config.get_github_project_urls()
            
            # Wenn wir bereits URLs haben, verwende sie
            if project_urls:
                projects = []
                for project_name, project_url in project_urls.items():
                    # Hole zusätzliche Informationen nur für relevante Projekte
                    project_info = self._get_basic_project_info(project_name, project_url)
                    if project_info:
                        projects.append(project_info)
                
                logger.info(f"Erfolgreich {len(projects)} Projekte aus Cache geladen")
                return projects
            
            # Fallback: Direkte API-Abfrage (sollte selten verwendet werden)
            return self._fetch_projects_from_api(username)
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der GitHub-Projekte: {e}")
            return []
    
    def _get_basic_project_info(self, project_name: str, project_url: str) -> Optional[GitHubProject]:
        """Erstellt GitHubProject-Objekt mit grundlegenden Informationen"""
        try:
            # Bestimme Sprache basierend auf Projekt-Name/Pattern
            language = self._guess_language(project_name)
            
            # Generiere Beschreibung basierend auf Projekt-Name
            description = self._generate_description(project_name)
            
            # Generiere Topics basierend auf Projekt-Name
            topics = self._generate_topics(project_name)
            
            return GitHubProject(
                name=project_name,
                description=description,
                url=project_url,
                language=language,
                topics=topics,
                stars=0,  # Für Caching setzen wir das auf 0
                is_fork=False
            )
            
        except Exception as e:
            logger.error(f"Fehler bei der Erstellung von Projekt-Info für {project_name}: {e}")
            return None
    
    def _guess_language(self, project_name: str) -> str:
        """Bestimmt die Programmiersprache basierend auf Projekt-Name"""
        name_lower = project_name.lower()
        
        if any(keyword in name_lower for keyword in ['python', 'py', 'django', 'flask']):
            return 'Python'
        elif any(keyword in name_lower for keyword in ['js', 'javascript', 'node', 'react', 'vue']):
            return 'JavaScript'
        elif any(keyword in name_lower for keyword in ['java', 'spring']):
            return 'Java'
        elif any(keyword in name_lower for keyword in ['cpp', 'c++', 'cmake']):
            return 'C++'
        elif any(keyword in name_lower for keyword in ['go', 'golang']):
            return 'Go'
        else:
            return 'Python'  # Standard-Fallback
    
    def _generate_description(self, project_name: str) -> str:
        """Generiert eine Beschreibung basierend auf Projekt-Name"""
        name_lower = project_name.lower()
        
        if 'automatic' in name_lower and 'motivation' in name_lower:
            return 'KI-basiertes System zur automatischen Generierung von Motivationsschreiben'
        elif 'llm' in name_lower and 'ws' in name_lower:
            return 'Webscraping-System mit LLM-Integration für automatisierte Datenextraktion'
        elif 'auto' in name_lower and 'search' in name_lower and 'job' in name_lower:
            return 'Automatisierte Jobsuche mit Machine Learning-Algorithmen'
        elif 'scraper' in name_lower or 'scraping' in name_lower:
            return 'Automatisierte Datenextraktion und Webscraping-Tool'
        elif 'bot' in name_lower:
            return 'Automatisierter Bot für verschiedene Aufgaben'
        elif 'api' in name_lower:
            return 'RESTful API-Implementierung mit modernen Technologien'
        else:
            return f'{project_name} - Softwareentwicklungsprojekt'
    
    def _generate_topics(self, project_name: str) -> List[str]:
        """Generiert Topics basierend auf Projekt-Name"""
        name_lower = project_name.lower()
        topics = []
        
        if 'python' in name_lower or self._guess_language(project_name) == 'Python':
            topics.extend(['python', 'automation'])
        
        if 'ai' in name_lower or 'llm' in name_lower:
            topics.extend(['artificial-intelligence', 'machine-learning'])
        
        if 'web' in name_lower or 'scraping' in name_lower:
            topics.extend(['web-scraping', 'data-extraction'])
        
        if 'auto' in name_lower:
            topics.append('automation')
        
        if 'job' in name_lower:
            topics.append('job-search')
        
        if 'api' in name_lower:
            topics.append('api')
        
        return topics
    
    def _fetch_projects_from_api(self, username: str) -> List[GitHubProject]:
        """Fallback: Direkte API-Abfrage (mit Rate-Limiting-Schutz)"""
        try:
            # GitHub API-URL
            api_url = f"https://api.github.com/users/{username}/repos"
            
            # Headers für bessere Rate-Limiting-Behandlung
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'AutomaticMotivation/1.0'
            }
            
            # Token falls verfügbar
            if Config.GITHUB_API_TOKEN:
                headers['Authorization'] = f'token {Config.GITHUB_API_TOKEN}'
            
            # API-Aufruf
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            repos = response.json()
            projects = []
            
            for repo in repos:
                # Überspringe Forks (optional)
                if repo.get('fork', False):
                    continue
                
                project = GitHubProject(
                    name=repo.get('name', ''),
                    description=repo.get('description', '') or '',
                    url=repo.get('html_url', ''),
                    language=repo.get('language', '') or '',
                    topics=repo.get('topics', []),
                    stars=repo.get('stargazers_count', 0),
                    is_fork=repo.get('fork', False)
                )
                
                projects.append(project)
            
            # Sortiere nach Sternen (beliebteste zuerst)
            projects.sort(key=lambda x: x.stars, reverse=True)
            
            logger.info(f"Erfolgreich {len(projects)} Projekte von GitHub-API abgerufen")
            return projects
            
        except requests.RequestException as e:
            logger.error(f"Fehler beim Abrufen von GitHub-Projekten: {e}")
            return []
        except Exception as e:
            logger.error(f"Allgemeiner Fehler bei GitHub-Projekten: {e}")
            return []
    
    def select_relevant_projects(self, projects: List[GitHubProject], 
                               job_position: str, job_requirements: str, 
                               max_projects: int = 3) -> List[GitHubProject]:
        """
        Wählt die relevantesten Projekte für eine Stellenbewerbung aus
        
        Args:
            projects: Liste aller GitHub-Projekte
            job_position: Stellenbezeichnung
            job_requirements: Stellenanforderungen
            max_projects: Maximale Anzahl von Projekten
            
        Returns:
            Liste der relevantesten Projekte
        """
        try:
            if not projects:
                return []
            
            # Erstelle Projekt-Übersicht für das LLM
            project_overview = []
            for i, project in enumerate(projects[:20]):  # Limitiere auf Top 20
                project_info = f"""
                {i+1}. {project.name}
                   Beschreibung: {project.description}
                   Sprache: {project.language}
                   Topics: {', '.join(project.topics) if project.topics else 'Keine'}
                   Sterne: {project.stars}
                   URL: {project.url}
                """
                project_overview.append(project_info)
            
            projects_text = '\n'.join(project_overview)
            
            prompt = f"""
            Analysiere die folgenden GitHub-Projekte und wähle die {max_projects} relevantesten für eine Bewerbung aus:

            STELLENPOSITION: {job_position}
            STELLENANFORDERUNGEN: {job_requirements}

            VERFÜGBARE PROJEKTE:
            {projects_text}

            AUFGABE:
            Wähle die {max_projects} relevantesten Projekte aus, die am besten zur Stellenposition und den Anforderungen passen.
            
            Berücksichtige dabei:
            1. Technische Relevanz (Programmiersprachen, Frameworks)
            2. Fachliche Relevanz (Projekttyp, Branche)
            3. Projektqualität (Beschreibung, Sterne, Topics)
            4. Vielfalt (verschiedene Aspekte der Fähigkeiten zeigen)

            ANTWORT-FORMAT:
            Gib NUR die Nummern der ausgewählten Projekte zurück, getrennt durch Kommata.
            Beispiel: 1, 3, 7
            """
            
            messages = [
                SystemMessage(content="""Du bist ein Experte für die Auswahl relevanter Projekte für Bewerbungen. 
                Wähle die Projekte aus, die am besten zur Stellenposition passen und die Fähigkeiten des Bewerbers optimal präsentieren."""),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse die Antwort
            selected_numbers = []
            for num in response.content.strip().split(','):
                try:
                    selected_numbers.append(int(num.strip()) - 1)  # -1 für 0-basierte Indexierung
                except ValueError:
                    continue
            
            # Wähle die entsprechenden Projekte aus
            selected_projects = []
            for idx in selected_numbers:
                if 0 <= idx < len(projects[:20]):
                    selected_projects.append(projects[idx])
            
            logger.info(f"Erfolgreich {len(selected_projects)} relevante Projekte ausgewählt")
            return selected_projects[:max_projects]
            
        except Exception as e:
            logger.error(f"Fehler bei der Projektauswahl: {e}")
            # Fallback: Nimm die ersten 3 Projekte mit den meisten Sternen
            return projects[:max_projects]
    
    def format_projects_for_application(self, projects: List[GitHubProject]) -> str:
        """
        Formatiert die ausgewählten Projekte für die Verwendung in Bewerbungen
        
        Args:
            projects: Liste der ausgewählten Projekte
            
        Returns:
            Formatierter Text über die Projekte
        """
        if not projects:
            return ""
        
        project_descriptions = []
        for project in projects:
            description = f"'{project.name}' ({project.language}): {project.description}"
            if project.topics:
                description += f" [Topics: {', '.join(project.topics)}]"
            project_descriptions.append(description)
        
        return "; ".join(project_descriptions)
    
    def get_relevant_projects_for_job(self, github_url: str, job_position: str, 
                                    job_requirements: str, max_projects: int = 3) -> List[GitHubProject]:
        """
        Kompletter Workflow: Projekte abrufen und relevante auswählen
        
        Args:
            github_url: GitHub-Profil URL
            job_position: Stellenbezeichnung
            job_requirements: Stellenanforderungen
            max_projects: Maximale Anzahl von Projekten
            
        Returns:
            Liste der relevantesten Projekte
        """
        try:
            # Projekte abrufen
            all_projects = self.get_github_projects(github_url)
            
            if not all_projects:
                logger.warning("Keine GitHub-Projekte gefunden")
                return []
            
            # Relevante Projekte auswählen
            relevant_projects = self.select_relevant_projects(
                all_projects, job_position, job_requirements, max_projects
            )
            
            return relevant_projects
            
        except Exception as e:
            logger.error(f"Fehler im GitHub-Projekt-Workflow: {e}")
            return []
