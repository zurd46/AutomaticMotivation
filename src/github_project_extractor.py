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
        Ruft alle öffentlichen Repositories von GitHub ab
        
        Args:
            github_url: GitHub-Profil URL (z.B. https://github.com/username)
            
        Returns:
            List von GitHubProject-Objekten
        """
        try:
            # Extrahiere Username aus URL
            username = github_url.split('/')[-1]
            
            # GitHub API-URL
            api_url = f"https://api.github.com/users/{username}/repos"
            
            # API-Aufruf
            response = requests.get(api_url)
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
            
            logger.info(f"Erfolgreich {len(projects)} Projekte von GitHub abgerufen")
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
