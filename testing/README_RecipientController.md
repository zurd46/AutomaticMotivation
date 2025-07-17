# Testing - RecipientController

Diese Verzeichnis enthält Tests für die RecipientController-Funktionalität.

## Dateien

### `demo_recipient_controller.py`
Demonstration der RecipientController-Funktionalität mit verschiedenen Szenarien:
- Spezifische Kontaktperson (Jan Enz)
- Keine Kontaktperson
- Generische Kontaktperson (HR Team)
- Keine Kontaktperson und keine Adresse

**Ausführung:**
```bash
cd testing
python demo_recipient_controller.py
```

### `test_recipient_integration.py`
Vollständige Integration-Tests für den RecipientController:
- Normalisierung von Empfänger-Informationen
- Anrede-Generierung
- PDF- und DOCX-Generierung
- Validierung der Ergebnisse

**Ausführung:**
```bash
cd testing
python test_recipient_integration.py
```

## Funktionalitäten

### RecipientController
Der RecipientController normalisiert und validiert Empfänger-Informationen:

1. **Kontaktperson-Normalisierung:**
   - Fehlende Kontaktperson → Firmenname
   - Generische Kontaktperson (HR Team) → Firmenname
   - Spezifische Kontaktperson → Unverändert

2. **Adress-Normalisierung:**
   - Fehlende Adresse → Standard-Adresse (Firmenname, Ort)
   - Vorhandene Adresse → Bereinigung für Kompatibilität

3. **Anrede-Generierung:**
   - Spezifische Person → "Sehr geehrter Herr/Frau [Name]"
   - Firmenname/Generisch → "Sehr geehrte Damen und Herren"

## Erwartete Ergebnisse

### Szenario 1: Spezifische Kontaktperson
```
VOR:  Kontaktperson: 'Jan Enz'
NACH: Kontaktperson: 'Jan Enz'
      Anrede: 'Sehr geehrter Herr Enz,'
```

### Szenario 2: Keine Kontaktperson
```
VOR:  Kontaktperson: ''
NACH: Kontaktperson: 'TechCorp AG'
      Anrede: 'Sehr geehrte Damen und Herren,'
```

### Szenario 3: Generische Kontaktperson
```
VOR:  Kontaktperson: 'HR Team'
NACH: Kontaktperson: 'DataAnalytics GmbH'
      Anrede: 'Sehr geehrte Damen und Herren,'
```

### Szenario 4: Keine Kontaktperson und Adresse
```
VOR:  Kontaktperson: '', Adresse: ''
NACH: Kontaktperson: 'StartupXYZ', Adresse: 'StartupXYZ, Bern'
      Anrede: 'Sehr geehrte Damen und Herren,'
```

## Validierung

Die Tests validieren:
- ✅ Korrekte Normalisierung von Empfänger-Informationen
- ✅ Angemessene Anrede-Generierung
- ✅ PDF-Generierung ohne Fehler
- ✅ DOCX-Generierung ohne Fehler
- ✅ Konsistente Empfänger-Informationen in beiden Formaten

## Fehlerbehandlung

Die Tests behandeln:
- Fehlende Kontaktpersonen
- Generische Kontaktpersonen
- Fehlende Adressen
- Unvollständige Informationen
