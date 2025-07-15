"""
AutoMoti - Automatische Motivationsschreiben-Generierung

Dieses Paket enthält alle Module für die automatische Generierung von Motivationsschreiben
basierend auf Job-URLs und KI-Technologie.
"""

from .models import JobInfo, JobDescription, PersonalInfo, MotivationLetter
from .job_extractor import JobExtractor
from .ai_generator import AIGenerator
from .pdf_generator import PDFGenerator
from .docx_generator import DocxGenerator
from .llm_utils import LLMFactory

__version__ = "1.0.0"
__author__ = "AutoMoti Team"

__all__ = [
    "JobInfo",
    "JobDescription", 
    "PersonalInfo",
    "MotivationLetter",
    "JobExtractor",
    "AIGenerator",
    "PDFGenerator",
    "DocxGenerator",
    "LLMFactory"
]