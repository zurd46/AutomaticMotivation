from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import logging
from config.config import Config
from src.models import JobInfo, JobDescription, MotivationLetter

logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self):
        self.config = Config.get_llm_config()
        self.llm = self._initialize_llm()
        
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
                SystemMessage(content="""Du bist ein Experte für das Schreiben von Motivationsschreiben. 
                Erstelle ein professionelles, überzeugenes Motivationsschreiben auf Deutsch, das:
                1. Direkt auf die Stellenbeschreibung eingeht
                2. Relevante Erfahrungen und Fähigkeiten hervorhebt
                3. Begeisterung für die Position zeigt
                4. Eine klare Struktur hat (Einleitung, Hauptteil, Schluss)
                5. Formell aber persönlich ist"""),
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
        Erfahrung: {personal_info['experience']}
        Fähigkeiten: {personal_info['skills']}

        ANREDE:
        Verwende EXAKT diese Anrede: "{salutation}"
        
        ANFORDERUNGEN FÜR DAS MOTIVATIONSSCHREIBEN:
        1. Schreibe ein überzeugendes, professionelles Motivationsschreiben auf Deutsch
        2. Gehe direkt auf die Stellenbeschreibung und Anforderungen ein
        3. Zeige, wie die Erfahrungen und Fähigkeiten zur Position passen
        4. Verwende eine formelle aber persönliche Sprache
        5. Strukturiere das Schreiben in Einleitung, Hauptteil und Schluss
        6. WICHTIG: Verwende EXAKT die oben angegebene Anrede "{salutation}" - keine andere!
        7. Zeige Begeisterung für die Position und das Unternehmen
        8. Halte es prägnant aber aussagekräftig (ca. 300-400 Wörter)
        9. WICHTIG: Schreibe KEINE Grußformel (wie "Mit freundlichen Grüßen") oder Signatur am Ende
        10. WICHTIG: Schreibe KEINEN Namen am Ende des Textes
        11. WICHTIG: Beginne das Schreiben mit der angegebenen Anrede "{salutation}"

        Schreibe NUR den Inhalt des Motivationsschreibens, ohne Kopf- oder Fußzeilen, ohne Grußformel und ohne Signatur.
        Das Schreiben MUSS mit der Anrede "{salutation}" beginnen und mit dem letzten inhaltlichen Absatz enden.
        """
        
        return prompt
    
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
