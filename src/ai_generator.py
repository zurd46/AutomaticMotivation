from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import logging
from config.config import Config
from src.models import JobInfo, JobDescription, MotivationLetter
from src.github_project_extractor import GitHubProjectExtractor
from src.linkedin_extractor import LinkedInExtractor
from src.intelligent_job_analyzer import IntelligentJobAnalyzer, JobCategory

logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self):
        self.config = Config.get_llm_config()
        self.llm = self._initialize_llm()
        self.github_extractor = GitHubProjectExtractor()
        self.linkedin_extractor = LinkedInExtractor()
        self.job_analyzer = IntelligentJobAnalyzer()
        
    def _initialize_llm(self):
        """Initialisiert das LLM basierend auf der Konfiguration"""
        try:
            if self.config['provider'] == 'openrouter':
                # OpenRouter mit OpenAI-kompatibler API
                llm = ChatOpenAI(
                    api_key=self.config['api_key'],
                    base_url=self.config['base_url'],
                    model=self.config['model'],
                    temperature=0.7,
                    max_tokens=2000
                )
                logger.info(f"OpenRouter LLM initialisiert mit Model: {self.config['model']}")
            else:
                # Standard OpenAI
                llm = ChatOpenAI(
                    api_key=self.config['api_key'],
                    model=self.config['model'],
                    temperature=self.config['temperature'],
                    max_tokens=2000
                )
                logger.info(f"OpenAI LLM initialisiert mit Model: {self.config['model']}")
            
            return llm
            
        except Exception as e:
            logger.error(f"Fehler bei LLM-Initialisierung: {e}")
            raise
    
    def _generate_salutation(self, job_description: JobDescription) -> str:
        """Generiert die korrekte Anrede basierend auf der Kontaktperson"""
        if job_description.contact_person and job_description.contact_person != "Nicht angegeben":
            # Bestimme Geschlecht und Nachname aus dem Namen
            contact_name = job_description.contact_person.strip()
            
            # Erweiterte Geschlechtserkennung für häufige deutsche Vornamen
            male_names = ['Jan', 'Max', 'Alexander', 'Michael', 'Andreas', 'Thomas', 'Christian', 'Daniel', 'Stefan', 'Markus', 'Johannes', 'Sebastian', 'Matthias', 'Florian', 'Tobias']
            female_names = ['Anna', 'Maria', 'Julia', 'Laura', 'Sarah', 'Lisa', 'Katharina', 'Sandra', 'Nicole', 'Petra', 'Sabine', 'Andrea', 'Stephanie', 'Christina', 'Melanie']
            
            # Extrahiere Vor- und Nachname
            name_parts = contact_name.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0]
                last_name = name_parts[-1]
                
                # Bestimme Anrede basierend auf Vornamen
                if first_name in male_names:
                    return f"Sehr geehrter Herr {last_name},"
                elif first_name in female_names:
                    return f"Sehr geehrte Frau {last_name},"
                else:
                    # Fallback: Für unbekannte Namen, prüfe auf -a Endung (oft weiblich)
                    if first_name.endswith('a'):
                        return f"Sehr geehrte Frau {last_name},"
                    else:
                        return f"Sehr geehrter Herr {last_name},"
            else:
                # Nur ein Name gegeben
                return f"Sehr geehrte/r {contact_name},"
        else:
            # Keine Kontaktperson angegeben
            return "Sehr geehrte Damen und Herren,"
    
    def generate_motivation_letter(self, job_description: JobDescription, 
                                 personal_info: dict = None) -> MotivationLetter:
        """
        Generiert ein Motivationsschreiben basierend auf der Stellenbeschreibung
        
        Args:
            job_description: Extrahierte Stellenbeschreibung
            personal_info: Persönliche Informationen des Bewerbers
            
        Returns:
            MotivationLetter: Generiertes Motivationsschreiben
        """
        try:
            # Verwende Config-Werte falls personal_info nicht gegeben
            if personal_info is None:
                personal_info = Config.get_personal_info()
            
            # Intelligente Stellenanalyse durchführen (vor Prompt-Erstellung)
            job_analysis = self.job_analyzer.analyze_job(
                job_description.position,
                job_description.description,
                job_description.requirements
            )
            
            # Speichere die Analyse für späteren Zugriff
            self._current_job_analysis = job_analysis
            
            logger.info(f"Stellenanalyse: {job_analysis['category'].value} (Confidence: {job_analysis['analysis_confidence']:.2f})")
            
            # Prompt für die Motivationsschreiben-Generierung
            prompt = self._create_motivation_prompt(job_description, personal_info)
            
            # LLM-Aufruf mit neuer invoke Methode
            messages = [
                SystemMessage(content="""Du bist ein Experte für das Schreiben von überzeugenden Motivationsschreiben. 
                Erstelle ein professionelles, spezifisches Motivationsschreiben auf Deutsch, das:
                1. Direkt auf die Stellenbeschreibung und spezifische Anforderungen eingeht
                2. Konkrete Projekterfahrungen mit messbaren Erfolgen hervorhebt
                3. Spezifische Technologien und Kennzahlen erwähnt
                4. Beratungs- und Teamarbeitserfahrung betont
                5. Branchen-spezifische Kenntnisse demonstriert
                6. Eine klare Problem-Lösung-Erfolg Struktur verwendet
                7. Formell aber persönlich und überzeugend ist
                8. Konkrete Beispiele statt allgemeiner Aussagen nutzt"""),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            content = response.content
            
            # Post-Generation-Filter für IT-Support-Stellen
            if hasattr(self, '_current_job_analysis') and self._current_job_analysis['category'] == JobCategory.IT_SUPPORT:
                original_content = content
                content = self._remove_github_project_mentions(content)
                if original_content != content:
                    logger.info("IT-Support-Stelle: GitHub-Projekt-Erwähnungen aus Content entfernt")
                else:
                    logger.info("IT-Support-Stelle: Keine GitHub-Projekt-Erwähnungen im Content gefunden")
            
            # MotivationLetter-Objekt erstellen
            # Subject mit Position und Arbeitszeit kombinieren
            position_with_hours = job_description.position
            if job_description.working_hours and job_description.working_hours != "Nicht angegeben":
                position_with_hours = f"{job_description.position} {job_description.working_hours}"
            
            motivation_letter = MotivationLetter(
                recipient_company=job_description.company,
                recipient_company_address=job_description.address,
                recipient_name=job_description.contact_person or job_description.company,
                recipient_address=job_description.location,  # Nutze location für Kontaktperson-Adresse
                subject=f"Bewerbung als {position_with_hours}",
                content=content,
                sender_name=personal_info["name"],
                sender_address=personal_info["address"],
                sender_phone=personal_info["phone"],
                sender_email=personal_info["email"]
            )
            
            logger.info("Motivationsschreiben erfolgreich generiert")
            return motivation_letter
            
        except Exception as e:
            logger.error(f"Fehler bei Motivationsschreiben-Generierung: {e}")
            raise
    
    def _create_motivation_prompt(self, job_description: JobDescription, 
                                personal_info: dict) -> str:
        """Erstellt den Prompt für die Motivationsschreiben-Generierung"""
        
        # Generiere die korrekte Anrede
        salutation = self._generate_salutation(job_description)
        
        # Verwende die bereits durchgeführte Job-Analyse
        job_analysis = self._current_job_analysis
        
        # Hole relevante GitHub-Projekte nur für Entwickler-Stellen
        github_projects = []
        project_descriptions = ""
        
        # GitHub-Projekte sind hauptsächlich für Entwickler-Stellen relevant
        if personal_info.get('github') and job_analysis['category'] in [JobCategory.SOFTWARE_DEVELOPMENT, JobCategory.DATA_SCIENCE]:
            try:
                github_projects = self.github_extractor.get_relevant_projects_for_job(
                    personal_info['github'],
                    job_description.position,
                    job_description.requirements,
                    max_projects=3
                )
                
                if github_projects:
                    project_descriptions = self._format_projects_for_prompt(github_projects, job_analysis)
                    logger.info(f"Erfolgreich {len(github_projects)} relevante Projekte für Entwickler-Stelle ausgewählt")
                else:
                    logger.info("Keine relevanten GitHub-Projekte für diese Entwickler-Stelle gefunden")
                    
            except Exception as e:
                logger.error(f"Fehler beim Abrufen von GitHub-Projekten: {e}")
        else:
            if job_analysis['category'] == JobCategory.IT_SUPPORT:
                logger.info("IT-Support-Stelle: Keine GitHub-Projekte verwendet - Fokus auf Support-Erfahrung")
            else:
                logger.info(f"Stelle ({job_analysis['category'].value}): Keine GitHub-Projekte verwendet")
        
        # Hole LinkedIn-Informationen
        linkedin_info = ""
        try:
            linkedin_info = self.linkedin_extractor.format_profile_for_application(job_description.requirements)
            logger.info("LinkedIn-Profil-Informationen erfolgreich geladen")
        except Exception as e:
            logger.error(f"Fehler beim Abrufen von LinkedIn-Informationen: {e}")
        
        # Erstelle stellenspezifische Prompts basierend auf der Analyse
        specific_instructions = self._create_job_specific_instructions(job_analysis)
        
        prompt = f"""
        Erstelle ein professionelles Motivationsschreiben für folgende Stellenausschreibung:

        STELLENBESCHREIBUNG:
        Unternehmen: {job_description.company}
        Position: {job_description.position}
        Bereich: {job_description.department or 'Nicht angegeben'}
        Beschreibung: {job_description.description}
        
        Anforderungen:
        {job_description.requirements}
        
        Angebotene Leistungen:
        {job_description.benefits or 'Nicht angegeben'}
        
        Kontaktperson: {job_description.contact_person or 'Nicht angegeben'}
        Adresse: {job_description.address}

        INTELLIGENTE STELLENANALYSE:
        Kategorie: {job_analysis['category'].value}
        Confidence: {job_analysis['analysis_confidence']:.2f}
        Schlüsselanforderungen: {', '.join(job_analysis['key_requirements'])}
        Fokus-Bereiche: {', '.join(job_analysis['focus_recommendations']['focus_areas'])}
        Zu vermeiden: {', '.join(job_analysis['focus_recommendations']['avoid_areas'])}

        BEWERBER-INFORMATIONEN:
        Name: {personal_info['name']}
        GitHub: {personal_info['github']}
        LinkedIn: {Config.PERSONAL_LINKEDIN}
        Erfahrung: {personal_info['experience']}
        Fähigkeiten: {personal_info['skills']}

        RELEVANTE GITHUB-PROJEKTE:
        {project_descriptions if project_descriptions else 'Keine GitHub-Projekte für diese Stellenkategorie erforderlich'}

        LINKEDIN-PROFIL-INFORMATIONEN:
        {linkedin_info if linkedin_info else 'Keine LinkedIn-Informationen verfügbar'}

        ANREDE:
        Verwende EXAKT diese Anrede: "{salutation}"
        
        STELLENSPEZIFISCHE ANWEISUNGEN:
        {specific_instructions}
        """
        
        # Stelle-spezifische Schlusssätze basierend auf GitHub-Projekt-Verfügbarkeit
        if job_analysis['category'] == JobCategory.IT_SUPPORT or not project_descriptions:
            final_sentence = "Ich freue mich darauf, Sie in einem persönlichen Gespräch von meiner Motivation und Eignung zu überzeugen und dabei gezielt auf meine Qualifikationen sowie Ihre Fragen einzugehen."
        else:
            final_sentence = "Ich freue mich darauf, Sie in einem persönlichen Gespräch von meiner Motivation und Eignung zu überzeugen und dabei gezielt auf relevante Projekte sowie Ihre Fragen einzugehen."
        
        prompt += f"""
        ANFORDERUNGEN FÜR DAS MOTIVATIONSSCHREIBEN:
        1. Schreibe ein überzeugendes, professionelles Motivationsschreiben auf Deutsch
        2. Gehe direkt auf die Stellenbeschreibung und spezifische Anforderungen ein
        3. Zeige, wie die Erfahrungen und Fähigkeiten zur Position passen
        4. Verwende eine formelle aber persönliche Sprache
        5. Strukturiere das Schreiben in klar getrennte Absätze mit Leerzeilen dazwischen
        6. WICHTIG: Verwende EXAKT die oben angegebene Anrede "{salutation}" - keine andere!
        7. Zeige Begeisterung für die Position und das Unternehmen
        8. Halte es prägnant aber aussagekräftig (ca. 400-500 Wörter)
        9. WICHTIG: Schreibe KEINE Grußformel (wie "Mit freundlichen Grüßen") oder Signatur am Ende
        10. WICHTIG: Schreibe KEINEN Namen am Ende des Textes
        11. WICHTIG: Beginne das Schreiben mit der angegebenen Anrede "{salutation}"
        12. WICHTIG: Verwende EXAKT diesen Schlusssatz als letzten Absatz: "{final_sentence}"
        13. WICHTIG: Struktur mit Absätzen - Einleitung, 2-3 Hauptabsätze, Schluss - jeweils durch Leerzeilen getrennt
        """
        
        # Passe die Projektanweisungen basierend auf Stellenkategorie an
        if job_analysis['category'] in [JobCategory.SOFTWARE_DEVELOPMENT, JobCategory.DATA_SCIENCE] and project_descriptions:
            project_instructions = """
        SPEZIFISCHE VERBESSERUNGEN - VERWENDE DIE GITHUB-PROJEKTE UND LINKEDIN-INFORMATIONEN:
        13. Erwähne KONKRETE PROJEKTE aus der Liste oben mit spezifischen Technologien und messbaren Erfolgen
        14. Nenne KONKRETE ERFOLGE mit Kennzahlen (z.B. "Reduzierung der Prozesszeit um 40%", "Steigerung der Effizienz um 30%", "Verbesserung der Genauigkeit um 25%")
        15. Betone TEAMARBEIT und BERATUNGSERFAHRUNG mit konkreten Beispielen (z.B. "In interdisziplinären Teams von 5 Entwicklern leitete ich...", "Durch enge Zusammenarbeit mit 3 Stakeholdern...", "Als Berater unterstützte ich 10+ Kunden bei...")
        16. Erwähne BRANCHEN-SPEZIFISCHE Kenntnisse falls relevant (z.B. Fintech, Healthcare, E-Commerce, Manufacturing, Consulting)
        17. Verwende AKTIVE VERBEN und KONKRETE BEISPIELE statt allgemeiner Aussagen
            """
        else:
            project_instructions = """
        SPEZIFISCHE VERBESSERUNGEN - FOKUS AUF BERUFSERFAHRUNG OHNE GITHUB-PROJEKTE:
        13. ABSOLUT VERBOTEN: Erwähne KEINE GitHub-Projekte oder spezifische Programmierprojekte
        14. ABSOLUT VERBOTEN: Verwende NICHT die Begriffe "entwickelte", "programmierte", "implementierte", "Projekt"
        15. ABSOLUT VERBOTEN: Erwähne KEINE Technologien wie Python, JavaScript, Code, Development
        16. ABSOLUT VERBOTEN: Nenne KEINE spezifischen Software-Projekte wie Webp-to-JPG, AutomaticMotivation
        17. Konzentriere dich auf allgemeine Berufserfahrung und Fähigkeiten
        18. Betone deine Arbeitsweise, Soft Skills und Lernbereitschaft
        19. Erwähne deine Fähigkeiten im Umgang mit verschiedenen Technologien und Tools
        20. Zeige deine Motivation und Bereitschaft, sich in neue Bereiche einzuarbeiten
        21. Verwende AKTIVE VERBEN wie "betreute", "unterstützte", "löste", "optimierte"
        22. Fokussiere auf Problemlösungsfähigkeiten und Kundenservice
        23. Betone KOMMUNIKATIONSFÄHIGKEITEN und Teamarbeit
        24. Erwähne PROZESSOPTIMIERUNG und EFFIZIENZSTEIGERUNG ohne spezifische Projekte
        25. Verwende Begriffe wie "Erfahrung", "Kenntnisse", "Fähigkeiten", "Expertise"
            """

        # Vervollständige den Prompt
        prompt += project_instructions
        
        return prompt
    
    def _generate_success_examples(self, project) -> str:
        """Generiert realistische Erfolgsbeispiele basierend auf dem Projekt-Typ"""
        success_templates = {
            'python': [
                "Effizienzsteigerung um 40-80%",
                "Reduzierung der Bearbeitungszeit um 30-60%",
                "Automatisierung von 70-90% der manuellen Prozesse",
                "Kosteneinsparung von 15-35%",
                "Verbesserung der Datenqualität um 85-95%"
            ],
            'javascript': [
                "Verbesserung der Benutzererfahrung um 40-70%",
                "Reduzierung der Ladezeiten um 50-80%",
                "Steigerung der Conversion-Rate um 20-45%",
                "Erhöhung der Nutzerinteraktion um 60-90%"
            ],
            'ai_ml': [
                "Verbesserung der Vorhersagegenauigkeit um 25-50%",
                "Reduzierung der Trainingszeit um 40-70%",
                "Automatisierung von 80-95% der Klassifizierungsaufgaben",
                "Steigerung der Erkennungsrate um 30-60%"
            ],
            'automation': [
                "Automatisierung von 70-95% der manuellen Tätigkeiten",
                "Reduzierung der Fehlerrate um 85-98%",
                "Zeitersparnis von 50-80% bei wiederkehrenden Aufgaben",
                "Verbesserung der Prozesskonsistenz um 90-95%"
            ],
            'web_scraping': [
                "Steigerung der Datenerfassung um 60-90%",
                "Reduzierung der Sammeldauer um 70-85%",
                "Verbesserung der Datenqualität um 80-95%",
                "Automatisierung von 85-95% der Datensammlung"
            ]
        }
        
        # Bestimme Projekt-Typ basierend auf Name und Technologie
        project_lower = project.name.lower()
        language_lower = project.language.lower() if project.language else ""
        
        if any(keyword in project_lower for keyword in ['ai', 'ml', 'machine', 'learning', 'llm']):
            return '; '.join(success_templates['ai_ml'][:2])
        elif any(keyword in project_lower for keyword in ['auto', 'automatic', 'automation']):
            return '; '.join(success_templates['automation'][:2])
        elif any(keyword in project_lower for keyword in ['scraping', 'scraper', 'crawler']):
            return '; '.join(success_templates['web_scraping'][:2])
        elif 'python' in language_lower:
            return '; '.join(success_templates['python'][:2])
        elif language_lower in ['javascript', 'typescript']:
            return '; '.join(success_templates['javascript'][:2])
        else:
            return '; '.join(success_templates['python'][:2])  # Standard fallback
    
    def _create_job_specific_instructions(self, job_analysis: dict) -> str:
        """Erstellt stellenspezifische Anweisungen basierend auf der Jobanalyse"""
        
        category = job_analysis['category']
        focus_areas = job_analysis['focus_recommendations']['focus_areas']
        avoid_areas = job_analysis['focus_recommendations']['avoid_areas']
        key_phrases = job_analysis['focus_recommendations']['key_phrases']
        
        if category == JobCategory.IT_SUPPORT:
            return f"""
            KRITISCH FÜR IT-SUPPORT-POSITION:
            
            FOKUS AUF FOLGENDE BEREICHE:
            {', '.join(focus_areas)}
            
            UNBEDINGT VERMEIDEN:
            {', '.join(avoid_areas)}
            
            VERWENDE DIESE SCHLÜSSELPHRASEN:
            {', '.join(key_phrases)}
            
            SPEZIFISCHE ANWEISUNGEN FÜR IT-SUPPORT:
            - Betone KUNDENSERVICE und BENUTZERUNTERSTÜTZUNG als Kernkompetenzen
            - Erwähne TROUBLESHOOTING und PROBLEMLÖSUNG als Hauptfähigkeiten
            - Fokussiere auf SYSTEMADMINISTRATION und HARDWARE-/SOFTWARE-SUPPORT
            - Verwende Begriffe wie "Anwenderbetreuung", "Servicedesk", "First-Level-Support"
            - Betone KOMMUNIKATIONSFÄHIGKEITEN für Endbenutzer-Support
            - Erwähne TICKETING-SYSTEME und SERVICE-MANAGEMENT-Erfahrung
            - Fokussiere auf HANDS-ON-MENTALITÄT und praktische Problemlösung
            - Vermeide Entwicklungs-spezifische Begriffe wie "Coding", "Development", "Programming"
            - Betone SERVICEORIENTIERUNG und HILFSBEREITSCHAFT
            - Erwähne SCHULUNGEN und WISSENSVERMITTLUNG für Endbenutzer
            
            ABSOLUT VERBOTEN FÜR IT-SUPPORT:
            - KEINE GitHub-Projekte erwähnen
            - KEINE Programmier-Projekte erwähnen  
            - KEINE Software-Entwicklungsprojekte erwähnen
            - KEINE Code-Beispiele erwähnen
            - KEINE Webp-to-JPG oder ähnliche Projekte erwähnen
            - KEINE Automatisierungsprojekte erwähnen
            - KEINE technischen Implementierungsprojekte erwähnen
            - KEINE Begriffe wie "entwickelte", "programmierte", "implementierte" verwenden
            - KEINE Erwähnung von Python, JavaScript, Code, Development
            - NIEMALS das Wort "Projekt" im Zusammenhang mit Entwicklung verwenden
            
            STATTDESSEN ERWÄHNE:
            - Berufserfahrung im IT-Support
            - Kundenservice-Erfahrung
            - Troubleshooting-Fähigkeiten
            - Systemadministration-Kenntnisse
            - Benutzerschulung und -betreuung
            - Prozessoptimierung im Support-Bereich
            - Servicedesk-Erfahrung
            - Ticketing-System-Kenntnisse
            - Lösungsorientierte Arbeitsweise
            - Kommunikation mit Endanwendern
            - Technische Dokumentation
            - Hardware- und Software-Betreuung
            """
        
        elif category == JobCategory.SOFTWARE_DEVELOPMENT:
            return f"""
            FOKUS AUF ENTWICKLUNG:
            
            FOKUS AUF FOLGENDE BEREICHE:
            {', '.join(focus_areas)}
            
            VERWENDE DIESE SCHLÜSSELPHRASEN:
            {', '.join(key_phrases)}
            
            SPEZIFISCHE ANWEISUNGEN FÜR SOFTWARE-ENTWICKLUNG:
            - Betone PROGRAMMIERUNG und CODE-ENTWICKLUNG
            - Erwähne FRAMEWORKS und ENTWICKLUNGSTOOLS
            - Fokussiere auf SOFTWARE-ARCHITEKTUR und DESIGN-PATTERNS
            - Verwende Begriffe wie "Coding", "Development", "Implementation"
            - Betone AGILE METHODEN und SCRUM-Erfahrung
            - Erwähne GIT und VERSION-CONTROL-Systeme
            """
        
        else:
            return f"""
            ALLGEMEINE STELLENANALYSE:
            
            FOKUS AUF FOLGENDE BEREICHE:
            {', '.join(focus_areas)}
            
            VERWENDE DIESE SCHLÜSSELPHRASEN:
            {', '.join(key_phrases)}
            
            PASSE DEINE SPRACHE AN DIE STELLENKATEGORIE AN
            """
    
    def _format_projects_for_prompt(self, projects, job_analysis: dict = None) -> str:
        """Formatiert GitHub-Projekte für den Prompt mit stellenspezifischem Fokus"""
        if not projects:
            return ""
        
        category = job_analysis['category'] if job_analysis else JobCategory.UNKNOWN
        
        project_details = []
        for project in projects:
            # Erweiterte Projektbeschreibung mit stellenspezifischem Fokus
            enhanced_description = self._enhance_project_description(project, category)
            
            # Füge potenzielle Erfolgs-Kennzahlen basierend auf Projekt-Typ hinzu
            success_examples = self._generate_success_examples(project)
            
            details = f"""
            - Projekt: {project.name}
              Beschreibung: {enhanced_description}
              Technologie: {project.language}
              GitHub-URL: {project.url}
              Topics: {', '.join(project.topics) if project.topics else 'Keine'}
              Popularität: {project.stars} Sterne
              Potenzielle Erfolge: {success_examples}
              
              VERWENDUNG IN BEWERBUNG:
              {self._get_project_usage_instructions(project, category)}
            """
            project_details.append(details)
        
        return '\n'.join(project_details)
    
    def _enhance_project_description(self, project, category: JobCategory) -> str:
        """Erweitert Projektbeschreibung basierend auf Stellenkategorie"""
        
        base_description = project.description
        
        if category == JobCategory.IT_SUPPORT:
            # Fokus auf Support-relevante Aspekte
            if 'automatic' in project.name.lower():
                return f"{base_description} - Automatisierte Lösung zur Effizienzsteigerung im Support-Bereich"
            elif 'webp' in project.name.lower():
                return f"{base_description} - Tool zur Unterstützung von Anwendern bei Bildkonvertierung"
            else:
                return f"{base_description} - Unterstützungstool für verbesserte Benutzerexperience"
        
        elif category == JobCategory.SOFTWARE_DEVELOPMENT:
            # Fokus auf Entwicklungs-relevante Aspekte
            return f"{base_description} - Entwicklungsprojekt mit modernen Technologien"
        
        return base_description
    
    def _get_project_usage_instructions(self, project, category: JobCategory) -> str:
        """Gibt Anweisungen für die Verwendung des Projekts basierend auf Stellenkategorie"""
        
        if category == JobCategory.IT_SUPPORT:
            return f"""
            Erwähne dieses Projekt als Beispiel für:
            - Automatisierung zur Effizienzsteigerung im Support
            - Benutzerfreundliche Lösungen für technische Probleme
            - Prozessoptimierung und Workflow-Verbesserung
            - Technische Unterstützung und Serviceverbesserung
            VERMEIDE: Erwähnung von Programmiersprachen oder Code-Entwicklung
            """
        
        elif category == JobCategory.SOFTWARE_DEVELOPMENT:
            return f"""
            Erwähne dieses Projekt als Beispiel für:
            - Softwareentwicklung mit {project.language}
            - Technische Implementierung und Code-Qualität
            - Entwicklungsprozesse und Best Practices
            - Architektur und Design-Entscheidungen
            """
        
        return f"Erwähne dieses Projekt mit konkreten Technologien und messbaren Erfolgen"
    
    def extract_key_requirements(self, job_description: JobDescription) -> list:
        """
        Extrahiert die wichtigsten Anforderungen aus der Stellenbeschreibung
        
        Args:
            job_description: Stellenbeschreibung
            
        Returns:
            List der wichtigsten Anforderungen
        """
        try:
            prompt = f"""
            Analysiere die folgende Stellenbeschreibung und extrahiere die 5 wichtigsten Anforderungen:

            Position: {job_description.position}
            Beschreibung: {job_description.description}
            Anforderungen: {job_description.requirements}

            Gib nur die wichtigsten Anforderungen als Liste zurück, eine pro Zeile, ohne Nummerierung.
            """
            
            messages = [
                SystemMessage(content="Du bist ein Experte für die Analyse von Stellenbeschreibungen. Extrahiere die wichtigsten Anforderungen präzise und strukturiert."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            requirements = [req.strip() for req in response.content.split('\n') if req.strip()]
            
            logger.info(f"Wichtigste Anforderungen extrahiert: {requirements}")
            return requirements
            
        except Exception as e:
            logger.error(f"Fehler bei Anforderungsextraktion: {e}")
            return []

    def _remove_github_project_mentions(self, content):
        """
        Entfernt alle GitHub-Projekt-Erwähnungen aus dem Content
        """
        import re
        
        # Definiere Muster für GitHub-Projekt-Erwähnungen
        github_patterns = [
            r'GitHub-?[Pp]rojekt[e]?[^\.\n]*',
            r'[Pp]rojekt[e]?[^\.\n]*GitHub[^\.\n]*',
            r'Repository[^\.\n]*',
            r'[Rr]epo[^\.\n]*',
            r'[Ee]ntwicklung[^\.\n]*[Pp]rojekt[e]?[^\.\n]*',
            r'[Pp]rojekt[e]?[^\.\n]*[Ee]ntwicklung[^\.\n]*',
            r'[Cc]ode[^\.\n]*[Pp]rojekt[e]?[^\.\n]*',
            r'[Pp]rojekt[e]?[^\.\n]*[Cc]ode[^\.\n]*',
            r'[Pp]rogrammier[^\.\n]*[Pp]rojekt[e]?[^\.\n]*',
            r'[Aa]utomatisierung[^\.\n]*[Pp]rojekt[e]?[^\.\n]*',
            r'[Pp]rojekt[e]?[^\.\n]*[Aa]utomatisierung[^\.\n]*',
            r'[Ww]ebp-to-JPG[^\.\n]*',
            r'[Ss]oftware[^\.\n]*[Pp]rojekt[e]?[^\.\n]*',
            r'[Pp]rojekt[e]?[^\.\n]*[Ss]oftware[^\.\n]*',
            # Spezifische Ersetzungen für Standard-Phrasen
            r'auf relevante Projekte sowie Ihre Fragen einzugehen',
            r'relevante Projekte sowie Ihre Fragen',
            r'auf relevante Projekte',
            r'relevante Projekte'
        ]
        
        # Spezifische Ersetzungen für IT-Support
        replacements = {
            'auf relevante Projekte sowie Ihre Fragen einzugehen': 'auf meine Qualifikationen sowie Ihre Fragen einzugehen',
            'relevante Projekte sowie Ihre Fragen': 'meine Qualifikationen sowie Ihre Fragen',
            'auf relevante Projekte': 'auf meine Erfahrungen',
            'relevante Projekte': 'meine Qualifikationen'
        }
        
        # Führe spezifische Ersetzungen durch
        cleaned_content = content
        for original, replacement in replacements.items():
            cleaned_content = re.sub(original, replacement, cleaned_content, flags=re.IGNORECASE)
        
        # Entferne alle anderen gefundenen Muster
        for pattern in github_patterns:
            cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.IGNORECASE)
        
        # Bereinige doppelte Leerzeichen und Zeilen, aber erhalte Absätze
        cleaned_content = re.sub(r' +', ' ', cleaned_content)  # Nur mehrfache Leerzeichen
        cleaned_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_content)  # Dreifache+ Zeilenumbrüche zu doppelten
        cleaned_content = cleaned_content.strip()
        
        return cleaned_content
