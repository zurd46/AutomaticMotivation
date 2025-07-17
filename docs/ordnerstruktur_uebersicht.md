# Ordnerstruktur - AutomaticMotivation

## Übersicht der korrekten Dateiorganisation

### Hauptverzeichnis (`/`)
- `app.py` - Hauptanwendung
- `README.md` - Projektdokumentation
- `requirements.txt` - Python-Abhängigkeiten
- `.env` - Umgebungsvariablen

### Quellcode (`/src/`)
- `ai_generator.py` - KI-Generierung von Motivationsschreiben
- `job_extractor.py` - Extraktion von Stellenausschreibungen
- `pdf_generator.py` - PDF-Dokumentgenerierung
- `docx_generator.py` - DOCX-Dokumentgenerierung
- `recipient_controller.py` - **NEU**: Empfänger-Informationen-Kontrolle
- `models.py` - Datenmodelle
- `github_project_extractor.py` - GitHub-Projekt-Extraktion
- `intelligent_job_analyzer.py` - Intelligente Stellenanalyse

### Konfiguration (`/config/`)
- `config.py` - Konfigurationsverwaltung

### Tests (`/testing/`)
- `test_recipient_integration.py` - **NEU**: RecipientController-Integration-Tests
- `demo_recipient_controller.py` - **NEU**: RecipientController-Demonstration
- `README_RecipientController.md` - **NEU**: RecipientController-Dokumentation
- `run_all_tests.py` - Alle Tests ausführen
- `debug_*.py` - Debug-Skripte

### Skripte (`/scripts/`)
- `analyze_template.py` - Template-Analyse
- `create_full_test.py` - Vollständige Tests erstellen
- `update_personal_info.py` - Persönliche Informationen aktualisieren

### Dokumentation (`/docs/`)
- `recipient_controller_documentation.md` - **NEU**: RecipientController-Dokumentation
- `cleanup_summary.md` - Bereinigungs-Zusammenfassung
- `docx_feature_summary.md` - DOCX-Feature-Zusammenfassung
- `testing_README.md` - Test-Dokumentation

### Vorlagen (`/templates/`)
- `template.pdf` - PDF-Template

### Ausgabe (`/output/`)
- Generierte Motivationsschreiben (PDF und DOCX)

## Neue RecipientController-Funktionalität

### Implementierte Dateien:
1. **`src/recipient_controller.py`** - Hauptklasse für Empfänger-Kontrolle
2. **`testing/test_recipient_integration.py`** - Integration-Tests
3. **`testing/demo_recipient_controller.py`** - Demonstration
4. **`testing/README_RecipientController.md`** - Test-Dokumentation
5. **`docs/recipient_controller_documentation.md`** - Vollständige Dokumentation

### Integration:
- **`src/ai_generator.py`** - Erweitert um RecipientController-Integration
- Automatische Normalisierung von Empfänger-Informationen
- Verbesserte Anrede-Logik für Firmennamen

## Ausführung von Tests

### Aus dem testing/ Ordner:
```bash
cd testing
python demo_recipient_controller.py
python test_recipient_integration.py
```

### Aus dem Hauptverzeichnis:
```bash
python testing/demo_recipient_controller.py
python testing/test_recipient_integration.py
```

## Vorteile der korrekten Ordnerstruktur:

1. **Übersichtlichkeit**: Tests sind im `testing/` Ordner organisiert
2. **Wartbarkeit**: Klare Trennung zwischen Quellcode und Tests
3. **Skalierbarkeit**: Einfache Erweiterung um weitere Tests
4. **Dokumentation**: Jeder Ordner hat seine spezifische Dokumentation
5. **Konsistenz**: Einheitliche Struktur für alle Komponenten

## Fazit

Die RecipientController-Funktionalität ist jetzt vollständig implementiert und korrekt in der Ordnerstruktur organisiert. Alle Tests befinden sich im `testing/` Ordner und die Dokumentation ist im `docs/` Ordner verfügbar.
