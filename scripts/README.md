# 🛠️ Scripts - Hilfsskripte für AutomaticMotivation

Dieses Verzeichnis enthält verschiedene Hilfsskripte für Entwicklung, Tests und Wartung der AutomaticMotivation-Anwendung.

## 📁 Verfügbare Skripte

### 🧪 Test-Skripte

#### `test_motivation.py`
Erstellt ein einfaches Test-Motivationsschreiben basierend auf dem PDF-Template.

**Verwendung:**
```bash
python scripts/test_motivation.py
```

**Funktionen:**
- Erstellt Test-Job-Informationen für Datalynx AG
- Generiert ein Motivationsschreiben mit AI
- Speichert das Ergebnis als PDF

#### `create_full_test.py`
Vollständiges Test-System mit manuellen Job-Informationen.

**Verwendung:**
```bash
python scripts/create_full_test.py
```

**Funktionen:**
- Erstellt detaillierte Job-Informationen
- Zeigt Template-Analyse
- Generiert und speichert PDF

### 🔧 Entwicklungs-Tools

#### `test_docx_generation.py`
Testet die DOCX-Generierung mit Beispieldaten.

**Verwendung:**
```bash
python scripts/test_docx_generation.py
```

**Funktionen:**
- Erstellt Test-Job-Informationen
- Generiert DOCX-Dokument mit Beispieldaten
- Zeigt Dateiinformationen an
- Validiert DOCX-Erstellung

#### `debug_extraction.py`
Debug-Tool für die Job-Extraktion aus URLs.

**Verwendung:**
```bash
python scripts/debug_extraction.py
```

**Funktionen:**
- Testet HTML-Extraktion von Job-URLs
- Zeigt extrahierten Text an
- Überprüft Kontaktinformationen

#### `analyze_template.py`
Analysiert PDF-Templates und zeigt Informationen an.

**Verwendung:**
```bash
python scripts/analyze_template.py
```

**Funktionen:**
- Überprüft Template-Verfügbarkeit
- Zeigt Template-Eigenschaften
- Analysiert Textfelder

### ⚙️ Konfiguration

#### `update_personal_info.py`
Interaktives Tool zur Aktualisierung persönlicher Informationen.

**Verwendung:**
```bash
python scripts/update_personal_info.py
```

**Funktionen:**
- Zeigt aktuelle persönliche Daten
- Ermöglicht interaktive Aktualisierung
- Speichert Änderungen in .env Datei

## 🚀 Ausführung

Alle Skripte sollten aus dem Hauptverzeichnis des Projekts ausgeführt werden:

```bash
# Aus dem Hauptverzeichnis
cd /path/to/AutomaticMotivation
python scripts/script_name.py
```

## 📝 Hinweise

- Alle Skripte benötigen eine korrekt konfigurierte `.env` Datei
- Die Hauptanwendung sollte über `python app.py` gestartet werden
- Für Entwicklung und Tests können diese Skripte hilfreich sein
- Bei Problemen prüfen Sie zuerst die Log-Ausgaben

## 🔗 Abhängigkeiten

Die Skripte verwenden die gleichen Abhängigkeiten wie die Hauptanwendung:
- Alle Module aus `src/`
- Konfiguration aus `config/`
- Requirements aus `requirements.txt`
