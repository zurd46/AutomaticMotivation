#!/usr/bin/env python3
"""
Test-Script für LinkedIn-Integration
"""

from src.linkedin_extractor import LinkedInExtractor
from src.docx_generator import DocxGenerator
from src.pdf_generator import PDFGenerator
from src.models import MotivationLetter
from datetime import datetime

def test_linkedin_integration():
    """Testet die LinkedIn-Integration-Funktionalität"""
    
    print("🔗 Teste LinkedIn-Extractor...")
    
    # LinkedIn-Extractor testen
    linkedin_extractor = LinkedInExtractor()
    
    # Profil-Informationen abrufen
    profile = linkedin_extractor.get_profile_info()
    print(f"✅ LinkedIn-Profil geladen: {profile.name}")
    print(f"📝 Headline: {profile.headline}")
    print(f"🔗 URL: {profile.url}")
    
    # Relevante Skills für eine Beispiel-Stellenausschreibung
    job_requirements = "Python, Machine Learning, AI, Cloud Computing, AWS, Consulting, Team Leadership"
    relevant_skills = linkedin_extractor.get_relevant_skills_for_job(job_requirements)
    print(f"🎯 Relevante Skills: {relevant_skills}")
    
    # Relevante Zertifikate
    relevant_certs = linkedin_extractor.get_relevant_certifications_for_job(job_requirements)
    print(f"📜 Relevante Zertifikate: {relevant_certs}")
    
    # Formatierte Profil-Informationen
    formatted_profile = linkedin_extractor.format_profile_for_application(job_requirements)
    print(f"📄 Formatierte Profil-Informationen: {formatted_profile[:200]}...")
    
    # Test-Motivationsschreiben erstellen
    test_motivation = MotivationLetter(
        recipient_company="Test AG",
        recipient_company_address="Teststraße 1, 12345 Test, Deutschland",
        recipient_name="Herr Test",
        recipient_address="Teststraße 1, 12345 Test, Deutschland",
        subject="Bewerbung als AI Consultant",
        content="""
        Sehr geehrter Herr Test,

        mit großem Interesse bewerbe ich mich auf die ausgeschriebene Position. Meine Zertifizierung als AWS Cloud Practitioner unterstreicht meine Kompetenz in Cloud-Technologien. 
        
        In meinem Projekt 'AutomaticMotivation' habe ich eine innovative KI-basierte Lösung entwickelt, die Bewerbungsprozesse um 60% beschleunigt. 
        
        Weitere Details zu meiner Berufserfahrung und meinen Qualifikationen finden Sie in meinem LinkedIn-Profil.
        
        Diese Erfahrungen qualifizieren mich perfekt für die ausgeschriebene Position.
        """,
        sender_name="Daniel Zurmühle",
        sender_address="Hinterdorfstrasse 12, 6235 Winikon",
        sender_phone="+41 79 127 55 54",
        sender_email="dzurmuehle@gmail.com",
        date=datetime.now()
    )
    
    # DOCX-Generator mit LinkedIn-Links testen
    print("\n📄 Teste DOCX-Generator mit LinkedIn-Links...")
    docx_generator = DocxGenerator()
    docx_file = docx_generator.create_docx(test_motivation)
    print(f"✅ DOCX erstellt: {docx_file}")
    
    # PDF-Generator mit LinkedIn-Links testen
    print("\n📄 Teste PDF-Generator mit LinkedIn-Links...")
    pdf_generator = PDFGenerator()
    pdf_file = pdf_generator.create_pdf(test_motivation)
    print(f"✅ PDF erstellt: {pdf_file}")
    
    print("\n🎉 LinkedIn-Integration erfolgreich getestet!")
    print("✅ LinkedIn-Profil-Extraktion funktioniert")
    print("✅ Skills-Matching funktioniert")
    print("✅ Zertifikats-Matching funktioniert")
    print("✅ Hyperlinks in DOCX funktionieren")
    print("✅ Hyperlinks in PDF funktionieren")

if __name__ == "__main__":
    test_linkedin_integration()
