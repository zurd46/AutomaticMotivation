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
            'experience': cls.PERSONAL_EXPERIENCE,
            'skills': cls.PERSONAL_SKILLS
        }