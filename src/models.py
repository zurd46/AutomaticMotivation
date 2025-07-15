from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class JobInfo(BaseModel):
    """Datenmodell für extrahierte Job-Informationen"""
    url: str
    company: str  # Geändert von arbeitgeber zu company
    position: str
    department: Optional[str] = None  # Hinzugefügt
    address: str  # Geändert von adresse zu address
    contact_person: Optional[str] = None  # Geändert von kontaktperson zu contact_person
    contact_title: Optional[str] = None  # Titel der Kontaktperson
    email: Optional[str] = None
    phone: Optional[str] = None  # Geändert von telefon zu phone
    requirements: str = ""  # Geändert von List[str] zu str
    description: str = ""  # Geändert von beschreibung zu description
    benefits: Optional[str] = None  # Geändert von List[str] zu str
    working_hours: Optional[str] = None  # Geändert von arbeitszeit zu working_hours
    salary: Optional[str] = None  # Geändert von gehalt zu salary
    location: str = ""  # Geändert von standort zu location
    extracted_at: datetime = datetime.now()

# Alias für Kompatibilität
JobDescription = JobInfo

class PersonalInfo(BaseModel):
    """Datenmodell für persönliche Informationen"""
    name: str
    address: str  # Geändert von adresse zu address
    phone: str  # Geändert von telefon zu phone
    email: str
    profession: str  # Geändert von beruf zu profession
    experience: List[str] = []  # Geändert von erfahrung zu experience
    qualifications: List[str] = []  # Geändert von qualifikationen zu qualifications
    
class MotivationLetter(BaseModel):
    """Datenmodell für das Motivationsschreiben"""
    recipient_company: str  # Firmenname
    recipient_company_address: str  # Firmenadresse
    recipient_name: str
    recipient_address: str
    subject: str
    content: str
    sender_name: str
    sender_address: str
    sender_phone: str
    sender_email: str
    date: datetime = datetime.now()  # Geändert von datum zu date
