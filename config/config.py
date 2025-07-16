import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenRouter Konfiguration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3-sonnet')
    OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    
    # OpenAI Konfiguration (Fallback)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo-instruct')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Persönliche Informationen
    PERSONAL_NAME = os.getenv('PERSONAL_NAME', 'Max Mustermann')
    PERSONAL_ADDRESS = os.getenv('PERSONAL_ADDRESS', 'Musterstraße 1, 12345 Musterstadt')
    PERSONAL_PHONE = os.getenv('PERSONAL_PHONE', '+49 123 456789')
    PERSONAL_EMAIL = os.getenv('PERSONAL_EMAIL', 'max.mustermann@email.com')
    PERSONAL_GITHUB = os.getenv('PERSONAL_GITHUB', 'https://github.com/username')
    PERSONAL_LINKEDIN = os.getenv('PERSONAL_LINKEDIN', 'https://linkedin.com/in/username')
    PERSONAL_EXPERIENCE = os.getenv('PERSONAL_EXPERIENCE', '3 Jahre Berufserfahrung')
    PERSONAL_SKILLS = os.getenv('PERSONAL_SKILLS', 'Python, JavaScript, Projektmanagement')
    
    # App Settings
    USE_OPENROUTER = bool(OPENROUTER_API_KEY)
    
    @classmethod
    def get_llm_config(cls):
        """Gibt die bevorzugte LLM-Konfiguration zurück"""
        if cls.USE_OPENROUTER:
            return {
                'api_key': cls.OPENROUTER_API_KEY,
                'model': cls.OPENROUTER_MODEL,
                'base_url': cls.OPENROUTER_BASE_URL,
                'provider': 'openrouter'
            }
        else:
            return {
                'api_key': cls.OPENAI_API_KEY,
                'model': cls.OPENAI_MODEL,
                'temperature': cls.OPENAI_TEMPERATURE,
                'provider': 'openai'
            }
    
    @classmethod
    def get_personal_info(cls):
        """Gibt die persönlichen Informationen zurück"""
        return {
            'name': cls.PERSONAL_NAME,
            'address': cls.PERSONAL_ADDRESS,
            'phone': cls.PERSONAL_PHONE,
            'email': cls.PERSONAL_EMAIL,
            'github': cls.PERSONAL_GITHUB,
            'linkedin': cls.PERSONAL_LINKEDIN,
            'experience': cls.PERSONAL_EXPERIENCE,
            'skills': cls.PERSONAL_SKILLS
        }
    
    @classmethod
    def get_github_username(cls):
        """Extrahiert den GitHub-Username aus der PERSONAL_GITHUB URL"""
        if cls.PERSONAL_GITHUB:
            # Extrahiere Username aus URL: https://github.com/username -> username
            return cls.PERSONAL_GITHUB.split('/')[-1]
        return None
    
    @classmethod
    def get_github_project_urls(cls):
        """Gibt bekannte GitHub-Projekt-URLs zurück"""
        username = cls.get_github_username()
        if not username:
            return {}
        
        # Bekannte Projekte - könnte später aus API geladen werden
        known_projects = ['AutomaticMotivation', 'ZurdLLMWS', 'Auto-search-jobs']
        
        return {
            project: f'https://github.com/{username}/{project}'
            for project in known_projects
        }