#!/usr/bin/env python3
"""
Persönliche Informationen in .env konfigurieren
"""

import os
from dotenv import load_dotenv, set_key

def update_personal_info():
    """Aktualisiert persönliche Informationen in der .env Datei"""
    env_path = ".env"
    
    print("=" * 60)
    print("👤 Persönliche Informationen konfigurieren")
    print("=" * 60)
    
    # Aktuelle Werte laden
    load_dotenv()
    
    current_info = {
        'PERSONAL_NAME': os.getenv('PERSONAL_NAME', 'Max Mustermann'),
        'PERSONAL_ADDRESS': os.getenv('PERSONAL_ADDRESS', 'Musterstraße 1, 12345 Musterstadt'),
        'PERSONAL_PHONE': os.getenv('PERSONAL_PHONE', '+49 123 456789'),
        'PERSONAL_EMAIL': os.getenv('PERSONAL_EMAIL', 'max.mustermann@email.com'),
        'PERSONAL_EXPERIENCE': os.getenv('PERSONAL_EXPERIENCE', '3 Jahre Berufserfahrung'),
        'PERSONAL_SKILLS': os.getenv('PERSONAL_SKILLS', 'Python, JavaScript, Projektmanagement')
    }
    
    # Neue Werte eingeben
    new_info = {}
    
    print("📝 Aktuelle Werte anzeigen und neue eingeben (Enter = behalten):")
    print()
    
    for key, current_value in current_info.items():
        display_name = key.replace('PERSONAL_', '').replace('_', ' ').title()
        new_value = input(f"{display_name} [{current_value}]: ").strip()
        new_info[key] = new_value if new_value else current_value
    
    # Werte in .env speichern
    print("\n💾 Speichere Konfiguration...")
    
    for key, value in new_info.items():
        set_key(env_path, key, value)
        print(f"   ✅ {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ Persönliche Informationen erfolgreich aktualisiert!")
    print("=" * 60)
    print("💡 Diese Werte werden nun automatisch in der Anwendung verwendet.")
    print("💡 Sie können diese Datei jederzeit erneut ausführen, um Änderungen vorzunehmen.")

if __name__ == "__main__":
    update_personal_info()
