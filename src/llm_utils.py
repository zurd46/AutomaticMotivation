import logging
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from config.config import Config

logger = logging.getLogger(__name__)

class LLMFactory:
    """Factory für verschiedene LLM-Provider"""
    
    @staticmethod
    def create_llm(provider: str = None, model: str = None, **kwargs) -> Any:
        """
        Erstellt ein LLM basierend auf dem Provider
        
        Args:
            provider: 'openrouter' oder 'openai'
            model: Modell-Name
            **kwargs: Zusätzliche Parameter
            
        Returns:
            Initialisiertes LLM
        """
        config = Config.get_llm_config()
        
        if provider is None:
            provider = config['provider']
        
        if model is None:
            model = config['model']
            
        try:
            if provider == 'openrouter':
                return LLMFactory._create_openrouter_llm(model, **kwargs)
            elif provider == 'openai':
                return LLMFactory._create_openai_llm(model, **kwargs)
            else:
                raise ValueError(f"Unbekannter Provider: {provider}")
                
        except Exception as e:
            logger.error(f"Fehler bei LLM-Erstellung: {e}")
            raise
    
    @staticmethod
    def _create_openrouter_llm(model: str, **kwargs) -> ChatOpenAI:
        """Erstellt OpenRouter LLM"""
        default_params = {
            'temperature': 0.7,
            'max_tokens': 2000,
            'top_p': 1.0,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        }
        
        # Benutzerdefinierte Parameter überschreiben Standardwerte
        params = {**default_params, **kwargs}
        
        return ChatOpenAI(
            api_key=Config.OPENROUTER_API_KEY,
            base_url=Config.OPENROUTER_BASE_URL,
            model=model,
            **params
        )
    
    @staticmethod
    def _create_openai_llm(model: str, **kwargs) -> ChatOpenAI:
        """Erstellt OpenAI LLM"""
        default_params = {
            'temperature': Config.OPENAI_TEMPERATURE,
            'max_tokens': 2000
        }
        
        # Benutzerdefinierte Parameter überschreiben Standardwerte
        params = {**default_params, **kwargs}
        
        return ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model=model,
            **params
        )
    
    @staticmethod
    def get_available_models() -> Dict[str, list]:
        """
        Gibt verfügbare Modelle für jeden Provider zurück
        
        Returns:
            Dictionary mit Provider -> Liste der Modelle
        """
        return {
            'openrouter': [
                'anthropic/claude-3-opus',
                'anthropic/claude-3-sonnet',
                'anthropic/claude-3-haiku',
                'openai/gpt-4-turbo',
                'openai/gpt-4',
                'openai/gpt-3.5-turbo',
                'meta-llama/llama-2-70b-chat',
                'google/gemini-pro',
                'mistralai/mistral-7b-instruct',
                'cohere/command-r',
            ],
            'openai': [
                'gpt-4-turbo',
                'gpt-4',
                'gpt-3.5-turbo',
                'gpt-3.5-turbo-instruct'
            ]
        }
    
    @staticmethod
    def estimate_cost(provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Schätzt die Kosten für eine LLM-Anfrage
        
        Args:
            provider: Provider Name
            model: Modell Name
            input_tokens: Anzahl Input-Tokens
            output_tokens: Anzahl Output-Tokens
            
        Returns:
            Geschätzte Kosten in USD
        """
        # Grobe Kostenschätzung (Preise können variieren)
        pricing = {
            'openrouter': {
                'anthropic/claude-3-opus': {'input': 0.000015, 'output': 0.000075},
                'anthropic/claude-3-sonnet': {'input': 0.000003, 'output': 0.000015},
                'anthropic/claude-3-haiku': {'input': 0.00000025, 'output': 0.00000125},
                'openai/gpt-4-turbo': {'input': 0.00001, 'output': 0.00003},
                'openai/gpt-4': {'input': 0.00003, 'output': 0.00006},
                'openai/gpt-3.5-turbo': {'input': 0.0000005, 'output': 0.0000015},
            },
            'openai': {
                'gpt-4-turbo': {'input': 0.00001, 'output': 0.00003},
                'gpt-4': {'input': 0.00003, 'output': 0.00006},
                'gpt-3.5-turbo': {'input': 0.0000005, 'output': 0.0000015},
                'gpt-3.5-turbo-instruct': {'input': 0.0000015, 'output': 0.000002},
            }
        }
        
        if provider in pricing and model in pricing[provider]:
            model_pricing = pricing[provider][model]
            cost = (input_tokens * model_pricing['input']) + (output_tokens * model_pricing['output'])
            return round(cost, 6)
        
        return 0.0
    
    @staticmethod
    def get_model_info(provider: str, model: str) -> Dict[str, Any]:
        """
        Gibt Informationen über ein spezifisches Modell zurück
        
        Args:
            provider: Provider Name
            model: Modell Name
            
        Returns:
            Dictionary mit Modell-Informationen
        """
        model_info = {
            'openrouter': {
                'anthropic/claude-3-opus': {
                    'max_tokens': 4096,
                    'context_window': 200000,
                    'description': 'Anthropics mächtigstes Modell mit überlegener Leistung',
                    'strengths': ['Komplexe Aufgaben', 'Kreatives Schreiben', 'Analyse']
                },
                'anthropic/claude-3-sonnet': {
                    'max_tokens': 4096,
                    'context_window': 200000,
                    'description': 'Ausgewogenes Modell mit guter Leistung und Geschwindigkeit',
                    'strengths': ['Allgemeine Aufgaben', 'Textverarbeitung', 'Konversation']
                },
                'anthropic/claude-3-haiku': {
                    'max_tokens': 4096,
                    'context_window': 200000,
                    'description': 'Schnellstes Claude-Modell für einfache Aufgaben',
                    'strengths': ['Schnelle Antworten', 'Einfache Aufgaben', 'Kostengünstig']
                },
                'openai/gpt-4-turbo': {
                    'max_tokens': 4096,
                    'context_window': 128000,
                    'description': 'OpenAIs neuestes und leistungsfähigstes Modell',
                    'strengths': ['Komplexe Aufgaben', 'Code-Generierung', 'Analyse']
                },
                'openai/gpt-3.5-turbo': {
                    'max_tokens': 4096,
                    'context_window': 16385,
                    'description': 'Schnelles und kostengünstiges Modell für die meisten Aufgaben',
                    'strengths': ['Allgemeine Aufgaben', 'Konversation', 'Kostengünstig']
                }
            },
            'openai': {
                'gpt-4-turbo': {
                    'max_tokens': 4096,
                    'context_window': 128000,
                    'description': 'OpenAIs neuestes und leistungsfähigstes Modell',
                    'strengths': ['Komplexe Aufgaben', 'Code-Generierung', 'Analyse']
                },
                'gpt-4': {
                    'max_tokens': 4096,
                    'context_window': 8192,
                    'description': 'OpenAIs Flaggschiff-Modell mit hoher Leistung',
                    'strengths': ['Komplexe Aufgaben', 'Kreatives Schreiben', 'Problemlösung']
                },
                'gpt-3.5-turbo': {
                    'max_tokens': 4096,
                    'context_window': 16385,
                    'description': 'Schnelles und kostengünstiges Modell',
                    'strengths': ['Allgemeine Aufgaben', 'Konversation', 'Kostengünstig']
                }
            }
        }
        
        return model_info.get(provider, {}).get(model, {})
