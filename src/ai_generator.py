from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import logging
from config.config import Config
from src.models import JobInfo, JobDescription, MotivationLetter
from src.github_project_extractor import GitHubProjectExtractor
from src.linkedin_extractor import LinkedInExtractor

logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self):
        self.config = Config.get_llm_config()
        self.llm = self._initialize_llm()
        self.github_extractor = GitHubProjectExtractor()
        self.linkedin_extractor = LinkedInExtractor()
        
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
        
        # Hole relevante GitHub-Projekte
        github_projects = []
        project_descriptions = ""
        
        if personal_info.get('github'):
            try:
                github_projects = self.github_extractor.get_relevant_projects_for_job(
                    personal_info['github'],
                    job_description.position,
                    job_description.requirements,
                    max_projects=3
                )
                
                if github_projects:
                    project_descriptions = self._format_projects_for_prompt(github_projects)
                    logger.info(f"Erfolgreich {len(github_projects)} relevante Projekte für Bewerbung ausgewählt")
                else:
                    logger.warning("Keine relevanten GitHub-Projekte gefunden")
                    
            except Exception as e:
                logger.error(f"Fehler beim Abrufen von GitHub-Projekten: {e}")
        
        # Hole LinkedIn-Informationen
        linkedin_info = ""
        try:
            linkedin_info = self.linkedin_extractor.format_profile_for_application(job_description.requirements)
            logger.info("LinkedIn-Profil-Informationen erfolgreich geladen")
        except Exception as e:
            logger.error(f"Fehler beim Abrufen von LinkedIn-Informationen: {e}")
        
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

        BEWERBER-INFORMATIONEN:
        Name: {personal_info['name']}
        GitHub: {personal_info['github']}
        LinkedIn: {Config.PERSONAL_LINKEDIN}
        Erfahrung: {personal_info['experience']}
        Fähigkeiten: {personal_info['skills']}

        RELEVANTE GITHUB-PROJEKTE:
        {project_descriptions if project_descriptions else 'Keine spezifischen Projekte verfügbar'}

        LINKEDIN-PROFIL-INFORMATIONEN:
        {linkedin_info if linkedin_info else 'Keine LinkedIn-Informationen verfügbar'}

        ANREDE:
        Verwende EXAKT diese Anrede: "{salutation}"
        
        ANFORDERUNGEN FÜR DAS MOTIVATIONSSCHREIBEN:
        1. Schreibe ein überzeugendes, professionelles Motivationsschreiben auf Deutsch
        2. Gehe direkt auf die Stellenbeschreibung und spezifische Anforderungen ein
        3. Zeige, wie die Erfahrungen und Fähigkeiten zur Position passen
        4. Verwende eine formelle aber persönliche Sprache
        5. Strukturiere das Schreiben in Einleitung, Hauptteil und Schluss
        6. WICHTIG: Verwende EXAKT die oben angegebene Anrede "{salutation}" - keine andere!
        7. Zeige Begeisterung für die Position und das Unternehmen
        8. Halte es prägnant aber aussagekräftig (ca. 400-500 Wörter)
        9. WICHTIG: Schreibe KEINE Grußformel (wie "Mit freundlichen Grüßen") oder Signatur am Ende
        10. WICHTIG: Schreibe KEINEN Namen am Ende des Textes
        11. WICHTIG: Beginne das Schreiben mit der angegebenen Anrede "{salutation}"
        12. WICHTIG: Verwende EXAKT diesen Schlusssatz als letzten Absatz: "Ich freue mich darauf, Sie in einem persönlichen Gespräch von meiner Motivation und Eignung zu überzeugen und dabei gezielt auf relevante Projekte sowie Ihre Fragen einzugehen."
        
        SPEZIFISCHE VERBESSERUNGEN - VERWENDE DIE GITHUB-PROJEKTE UND LINKEDIN-INFORMATIONEN:
        13. Erwähne KONKRETE PROJEKTE aus der Liste oben mit spezifischen Technologien und messbaren Erfolgen
        14. Nenne KONKRETE ERFOLGE mit Kennzahlen (z.B. "Reduzierung der Prozesszeit um 40%", "Steigerung der Effizienz um 30%", "Verbesserung der Genauigkeit um 25%")
        15. Betone TEAMARBEIT und BERATUNGSERFAHRUNG mit konkreten Beispielen (z.B. "In interdisziplinären Teams von 5 Entwicklern leitete ich...", "Durch enge Zusammenarbeit mit 3 Stakeholdern...", "Als Berater unterstützte ich 10+ Kunden bei...")
        16. Erwähne BRANCHEN-SPEZIFISCHE Kenntnisse falls relevant (z.B. Fintech, Healthcare, E-Commerce, Manufacturing, Consulting)
        17. Verwende AKTIVE VERBEN und KONKRETE BEISPIELE statt allgemeiner Aussagen
        18. Zeige PROBLEM-LÖSUNG-ERFOLG Struktur in Beispielen (z.B. "Die Herausforderung X löste ich durch die Implementierung von Y, was zu einer Verbesserung von Z um 30% führte")
        19. Betone CONSULTANT-SPEZIFISCHE Fähigkeiten: Kundenberatung, Projektmanagement, Stakeholder-Management, Präsentationsfähigkeiten, Change Management
        20. Nutze die GitHub-Projekte als Belege für deine Kompetenz mit spezifischen Technologie-Stacks
        21. Erwähne spezifische Technologien und Frameworks aus den Projekten, die zur Stelle passen
        22. Zeige LEADERSHIP und INITIATIVE durch konkrete Beispiele
        23. Demonstriere PROBLEM-SOLVING Fähigkeiten mit spezifischen Szenarien
        24. Erwähne AGILE/SCRUM Erfahrung falls relevant
        25. Betone KOMMUNIKATIONSFÄHIGKEITEN mit Beispielen (Präsentationen, Workshops, Schulungen)
        26. Zeige KUNDENORIENTIERUNG durch konkrete Kundenprojekte oder -feedback
        27. NUTZE LINKEDIN-ZERTIFIKATE als Qualifikationsnachweis (z.B. "Meine Zertifizierung als AWS Cloud Practitioner unterstreicht meine Kompetenz in...")
        28. REFERENZIERE LINKEDIN-PROFIL als Verweis auf weitere Qualifikationen (z.B. "Weitere Details zu meiner Berufserfahrung finden Sie in meinem LinkedIn-Profil") - WICHTIG: Nur "LinkedIn-Profil" verlinken, NICHT die URL im Text anzeigen! KEINE spitzen Klammern <> verwenden!
        29. VERWENDE LINKEDIN-SKILLS passend zur Stellenausschreibung
        30. INTEGRIERE LINKEDIN-BERUFSERFAHRUNG in die Argumentation
        31. ERWÄHNE LINKEDIN-SPRACHEN falls relevant für die Position

        BEISPIEL-INTEGRATION VON GITHUB-PROJEKTEN MIT KONKRETEN ERFOLGEN:
        - "In meinem Projekt AutomaticMotivation entwickelte ich mit Python und OpenAI eine KI-basierte Lösung zur Automatisierung von Bewerbungsprozessen, die die Bearbeitungszeit um 60% reduzierte und die Erfolgsquote um 35% steigerte"
        - "Durch die Entwicklung von ZurdLLMWS mit Python und LangChain konnte ich ein automatisiertes Webscraping-System erstellen, das die Datenerfassung um 80% beschleunigte und bei der Prozessoptimierung unterstützte"
        - "In einem interdisziplinären Team leitete ich das Projekt Auto-search-jobs, welches durch Machine Learning-Algorithmen die Jobsuche automatisierte und viele Nutzer dabei unterstützte, passende Stellenangebote zu finden"
        - "Als technischer Berater begleitete ich verschiedene Kunden bei der Implementierung von KI-Lösungen, wobei ich durch Workshop-Formate und Präsentationen komplexe technische Konzepte verständlich vermittelte"
        - "Die Herausforderung der manuellen Datenverarbeitung löste ich durch die Implementierung eines Python-basierten Automatisierungssystems, was zu einer Kostenreduktion von 25% und einer Fehlerreduktion um 90% führte"
        
        WICHTIG ZU BEACHTEN: 
        - Erwähne UNBEDINGT mindestens 2-3 der folgenden Hauptprojekte in deinem Schreiben: AutomaticMotivation, ZurdLLMWS, Auto-search-jobs
        - Diese Projekte sollen als konkrete Beispiele für deine Kompetenz dienen
        - Verwende sie als Belege für deine Fähigkeiten in den jeweiligen Technologie-Stacks
        - WICHTIG: Verwende KEINE Anführungszeichen oder andere Sonderzeichen vor oder nach den GitHub-Projektnamen
        - Schreibe die Projektnamen direkt ohne Anführungszeichen: AutomaticMotivation, ZurdLLMWS, Auto-search-jobs
        - Erwähne NIEMALS spezifische Unternehmensnamen aus der LinkedIn-Berufserfahrung. Verwende stattdessen:
        - "In meiner beruflichen Laufbahn..."
        - "In verschiedenen Projekten..."
        - "Als Consultant..."
        - "In meiner Rolle als..."
        - "Bei meinen bisherigen Tätigkeiten..."

        Schreibe NUR den Inhalt des Motivationsschreibens, ohne Kopf- oder Fußzeilen, ohne Grußformel und ohne Signatur.
        Das Schreiben MUSS mit der Anrede "{salutation}" beginnen und mit dem letzten inhaltlichen Absatz enden.
        """
        
        return prompt
    
    def _format_projects_for_prompt(self, projects) -> str:
        """Formatiert GitHub-Projekte für den Prompt mit erweiterten Details"""
        if not projects:
            return ""
        
        project_details = []
        for project in projects:
            # Erweiterte Projektbeschreibung mit Erfolgs-Potenzial
            enhanced_description = project.description
            
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
              Erwähne dieses Projekt mit konkreten Technologien ({project.language}) und 
              erfundenen aber realistischen Kennzahlen aus den "Potenziellen Erfolgen".
              Zeige Problem-Lösung-Erfolg Struktur auf.
            """
            project_details.append(details)
        
        return '\n'.join(project_details)
    
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
