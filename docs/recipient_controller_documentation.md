# RecipientController - Dokumentation

## Überblick

Der `RecipientController` ist eine neue Komponente der AutomaticMotivation-Anwendung, die die Empfänger-Informationen von Stellenausschreibungen intelligent normalisiert und validiert.

## Problem

Ursprünglich führten fehlende oder unvollständige Kontaktangaben in Stellenausschreibungen zu:
- Fehlenden Empfänger-Informationen in Motivationsschreiben
- Inkonsistenten Anreden zwischen PDF und DOCX
- Unvollständigen Firmenadresse-Informationen

## Lösung

### 1. RecipientController-Klasse (`src/recipient_controller.py`)

**Hauptfunktionen:**
- `normalize_recipient_info()`: Normalisiert Empfänger-Informationen
- `validate_recipient_info()`: Validiert und gibt Empfehlungen
- `_normalize_contact_person()`: Behandelt Kontaktperson-Normalisierung
- `_normalize_company_address()`: Behandelt Adress-Normalisierung

**Intelligente Logik:**
- Erkennt fehlende Kontaktpersonen und setzt Firmenname als Fallback
- Erkennt generische Kontaktpersonen (HR Team, etc.) und ersetzt sie
- Erstellt Standard-Adressen wenn keine Firmenadresse verfügbar
- Bereinigt Adressen für bessere Kompatibilität

### 2. Integration in AIGenerator (`src/ai_generator.py`)

**Verbesserungen:**
- Automatische Normalisierung vor der Motivationsschreiben-Generierung
- Erweiterte Anrede-Logik für Firmennamen
- Validierung und Logging von Empfänger-Problemen

**Neue Anrede-Logik:**
```python
def _generate_salutation(self, job_description: JobDescription) -> str:
    # Erkennt Firmennamen und generiert "Sehr geehrte Damen und Herren,"
    # Erkennt spezifische Personen und generiert personalisierte Anrede
    # Behandelt generische Kontaktpersonen intelligent
```

## Verwendung

### Automatische Integration

Der RecipientController wird automatisch in der normalen Anwendung verwendet:

```python
from src.ai_generator import AIGenerator
from src.models import JobDescription

# Normale Verwendung - RecipientController wird automatisch angewendet
ai_generator = AIGenerator()
motivation_letter = ai_generator.generate_motivation_letter(job_description)
```

### Manuelle Verwendung

```python
from src.recipient_controller import RecipientController

controller = RecipientController()

# Normalisierung
normalized_job = controller.normalize_recipient_info(job_description)

# Validierung
validation = controller.validate_recipient_info(job_description)
```

## Testfälle

### Test 1: Keine Kontaktperson
```
VOR:  Kontaktperson: ''
NACH: Kontaktperson: 'TechCorp AG'
      Anrede: 'Sehr geehrte Damen und Herren,'
```

### Test 2: Generische Kontaktperson
```
VOR:  Kontaktperson: 'HR Team'
NACH: Kontaktperson: 'DataAnalytics GmbH'
      Anrede: 'Sehr geehrte Damen und Herren,'
```

### Test 3: Spezifische Kontaktperson
```
VOR:  Kontaktperson: 'Jan Enz'
NACH: Kontaktperson: 'Jan Enz'
      Anrede: 'Sehr geehrter Herr Enz,'
```

### Test 4: Keine Adresse
```
VOR:  Adresse: ''
NACH: Adresse: 'StartupXYZ, Bern'
```

## Erkannte Patterns

### Generische Kontaktpersonen (werden ersetzt):
- "HR Team"
- "Human Resources"
- "Personalabteilung"
- "Recruiting"
- "Bewerbung"

### Firmenname-Indikatoren (führen zu generischer Anrede):
- AG, GmbH, Ltd, Inc, Corp
- Solutions, Technologies, Services
- Group, Company, Enterprises

### Personalisierte Anrede-Erkennung:
- Bekannte Vornamen → "Sehr geehrter Herr/Frau [Nachname]"
- Firmennamen → "Sehr geehrte Damen und Herren"
- Generische Kontakte → "Sehr geehrte Damen und Herren"

## Vorteile

1. **Robustheit**: Keine fehlenden Empfänger-Informationen mehr
2. **Konsistenz**: Einheitliche Anrede-Behandlung zwischen PDF und DOCX
3. **Intelligenz**: Automatische Erkennung und Behandlung verschiedener Kontakttypen
4. **Kompatibilität**: Bereinigung von Adressen für bessere Dateiname-Kompatibilität
5. **Validierung**: Warnungen und Empfehlungen für Datenqualität

## Logs und Debugging

Der RecipientController loggt seine Aktivitäten:
```
INFO: Keine Kontaktperson gefunden, verwende Firmenname: TechCorp AG
INFO: Generische Kontaktperson gefunden (HR Team), verwende Firmenname: DataAnalytics GmbH
WARNING: Empfänger-Informationen Warnungen: ['Keine spezifische Kontaktperson gefunden']
```

## Erweiterung

Für neue Erkennungspatterns können folgende Bereiche erweitert werden:
- `generic_contacts` Liste für neue generische Kontakttypen
- `male_names`/`female_names` für neue Vornamen
- Firmenname-Erkennungslogik für neue Patterns
