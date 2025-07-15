# AutoMoti Testing Suite

Dieser Ordner enthält Debug- und Test-Scripts für die Job-Extraktion des AutoMoti-Systems.

## 🔍 Verfügbare Tests

### 1. HTML-Struktur-Analyse
**Datei:** `debug_html_extraction.py`
- Analysiert die HTML-Struktur der Job-Seite
- Sucht nach strukturierten Daten, Meta-Tags, Kontaktinformationen
- Extrahiert Emails, Telefonnummern, Adressen
- Speichert Ergebnisse in JSON-Format

### 2. LLM-Antwort-Parsing
**Datei:** `debug_llm_parsing.py`
- Testet die LLM-basierte Extraktion mit Beispiel-Text
- Zeigt rohe LLM-Antworten und geparste Ergebnisse
- Analysiert Erfolg der Extraktion verschiedener Felder
- Speichert Prompt, Antwort und Ergebnisse

### 3. Komplette Job-Extraktion
**Datei:** `debug_llm_extraction.py`
- Testet den kompletten Job-Extraktions-Workflow
- Lädt HTML, extrahiert Text, führt LLM-Extraktion durch
- Zeigt detaillierte Ergebnisse und Probleme
- Speichert alle Daten für weitere Analyse

### 4. Master-Test-Suite
**Datei:** `run_all_tests.py`
- Führt alle Tests in der richtigen Reihenfolge aus
- Erstellt umfassende Test-Zusammenfassung
- Gibt Empfehlungen für Verbesserungen
- Speichert alle Ergebnisse

## 🚀 Verwendung

### Einzelne Tests ausführen:
```bash
cd testing
python debug_html_extraction.py
python debug_llm_parsing.py
python debug_llm_extraction.py
```

### Alle Tests ausführen:
```bash
cd testing
python run_all_tests.py
```

## 📊 Ausgabe-Dateien

Alle Test-Ergebnisse werden im `testing/` Ordner gespeichert:
- `html_analysis_YYYYMMDD_HHMMSS.json` - HTML-Analyse-Ergebnisse
- `llm_response_YYYYMMDD_HHMMSS.json` - LLM-Antwort-Analyse
- `job_extraction_YYYYMMDD_HHMMSS.json` - Job-Extraktions-Ergebnisse
- `test_summary_YYYYMMDD_HHMMSS.json` - Zusammenfassung aller Tests

## 🔧 Konfiguration

Die Tests verwenden die gleiche Konfiguration wie das Haupt-System:
- `.env` Datei für API-Keys
- `config/config.py` für LLM-Einstellungen

## 🐛 Debugging-Tipps

1. **Unternehmen nicht extrahiert:**
   - Überprüfe HTML-Struktur nach Firmen-Keywords
   - Verbessere LLM-Prompt für Unternehmenserkennung

2. **Kontaktperson nicht extrahiert:**
   - Analysiere Kontakt-Bereiche in HTML
   - Erweitere Kontakt-Pattern im LLM-Prompt

3. **Email/Telefon nicht extrahiert:**
   - Prüfe ob Kontaktdaten in HTML vorhanden sind
   - Verbessere RegEx-Pattern für Extraktion

4. **Adresse nicht extrahiert:**
   - Suche nach Arbeitsort-Informationen
   - Erweitere Adress-Erkennungslogik

## 📋 Test-URL

Standard-Test-URL: https://datalynx.onlyfy.jobs/job/5yh3u42r7oxaiqj5pbomhh1xsbi68op

Erwartete Ergebnisse:
- **Unternehmen:** Datalynx AG
- **Position:** AI Consultant (m/w/d)
- **Kontaktperson:** Jan Schmitz-Elsen
- **Email:** jan.schmitz@datalynx.ch
- **Telefon:** +41 79 425 10 45
- **Standort:** Basel
