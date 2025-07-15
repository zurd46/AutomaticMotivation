# 🚀 AutomaticMotivation - Automatische Motivationsschreiben-Generierung

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-beta-orange.svg)

**AutomaticMotivation** ist ein KI-gestütztes Tool zur automatischen Generierung von personalisierten Motivationsschreiben basierend auf Stellenausschreibungen. Das System extrahiert automatisch relevante Informationen aus Job-URLs und erstellt professionelle Motivationsschreiben im deutschen Standard-Format.

## ✨ Features

- 🔍 **Automatische Job-Extraktion** - Extrahiert Stelleninformationen aus URLs
- 🤖 **KI-basierte Generierung** - Nutzt fortschrittliche LLM-Modelle (OpenAI, OpenRouter)
- 📄 **PDF-Generierung** - Erstellt professionelle PDFs im deutschen Standard-Format
- 📄 **DOCX-Generierung** - Zusätzliche Microsoft Word-Dokumente für einfache Bearbeitung
- 🎨 **Template-Support** - Unterstützt anpassbare PDF-Vorlagen
- 💻 **Rich Interface** - Moderne Konsolen-UI mit Panels und Tabellen
- 🌐 **Multi-Provider** - Unterstützt OpenAI und OpenRouter
- 📊 **Strukturierte Ausgabe** - Übersichtliche Zusammenfassungen und Statistiken

## 📋 Voraussetzungen

- Python 3.8 oder höher
- Git (für die Installation)
- Ein API-Key für OpenAI oder OpenRouter
- Internetverbindung für die Job-Extraktion

## 🔧 Installation

### 1. Repository klonen

```bash
git clone https://github.com/zurd46/AutomaticMotivation.git
cd AutomaticMotivation
```

### 2. Virtuelle Umgebung erstellen (empfohlen)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## ⚙️ Konfiguration

### 1. Umgebungsvariablen einrichten

Erstellen Sie eine `.env` Datei im Projektverzeichnis:

```bash
cp .env.example .env
```

### 2. .env Datei konfigurieren

Öffnen Sie die `.env` Datei und passen Sie die Werte an:

```properties
# Optional: Logging Level
LOG_LEVEL=INFO

# Persönliche Informationen für Motivationsschreiben
PERSONAL_NAME=Ihr Name
PERSONAL_ADDRESS=Ihre Straße 123, PLZ Ort
PERSONAL_PHONE=+49 123 456789
PERSONAL_EMAIL=ihre.email@example.com
PERSONAL_EXPERIENCE=X+ Jahre Berufserfahrung
PERSONAL_SKILLS=Python, JavaScript, TypeScript, etc.

# OpenRouter API Konfiguration (empfohlen)
OPENROUTER_API_KEY=sk-or-v1-ihr-api-key
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Fallback: OpenAI API Konfiguration
OPENAI_API_KEY=sk-proj-ihr-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo-instruct
OPENAI_TEMPERATURE=0.7
```

### 3. API-Keys erhalten

#### OpenRouter (empfohlen)
1. Besuchen Sie [OpenRouter.ai](https://openrouter.ai/)
2. Erstellen Sie ein kostenloses Konto
3. Gehen Sie zu "API Keys" und erstellen Sie einen neuen Key
4. Fügen Sie den Key in die `.env` Datei ein

#### OpenAI (Alternative)
1. Besuchen Sie [OpenAI Platform](https://platform.openai.com/)
2. Erstellen Sie ein Konto und fügen Sie Guthaben hinzu
3. Gehen Sie zu "API Keys" und erstellen Sie einen neuen Key
4. Fügen Sie den Key in die `.env` Datei ein

## 🚀 Verwendung

### Grundlegende Verwendung

```bash
python app.py
```

### Schritt-für-Schritt Anleitung

1. **Starten Sie die Anwendung**
   ```bash
   python app.py
   ```

2. **Modell auswählen** (optional)
   - Das System zeigt verfügbare KI-Modelle an
   - Wählen Sie ein Modell oder behalten Sie das Standard-Modell bei

3. **Job-URL eingeben**
   - Geben Sie die URL der Stellenausschreibung ein
   - Unterstützte Plattformen: StepStone, Indeed, LinkedIn, etc.

4. **Persönliche Daten überprüfen**
   - Das System lädt Ihre Daten aus der `.env` Datei
   - Sie können die Daten bei Bedarf anpassen

5. **Warten Sie auf die Generierung**
   - Job-Informationen werden extrahiert
   - Motivationsschreiben wird generiert
   - PDF wird erstellt

6. **Ergebnis erhalten**
   - Das PDF wird im `output/` Ordner gespeichert
   - Eine identische DOCX-Datei wird ebenfalls erstellt
   - Dateiname: `Motivationsschreiben_Firmenname_Ort_TTMMJJ.pdf/docx`

## 📁 Projektstruktur

```
AutomaticMotivation/
├── app.py                    # 🚀 Hauptanwendung
├── requirements.txt          # 📦 Python-Abhängigkeiten
├── .env                     # 🔐 Konfigurationsdatei (nicht in Git)
├── .env.example             # 📝 Beispiel-Konfiguration
├── .gitignore               # 🚫 Git-Ignore-Regeln
├── README.md                # 📖 Diese Datei
├── config/
│   └── config.py            # ⚙️ Konfigurationsverwaltung
├── src/                     # 📚 Hauptquellcode
│   ├── __init__.py
│   ├── models.py            # 🗂️ Datenmodelle
│   ├── job_extractor.py     # 🔍 Job-Informationen extrahieren
│   ├── ai_generator.py      # 🤖 KI-basierte Generierung
│   ├── pdf_generator.py     # 📄 PDF-Erstellung
│   ├── docx_generator.py    # 📄 DOCX-Erstellung
│   ├── template_pdf_generator.py  # 🎨 Template-basierte PDF-Erstellung
│   └── llm_utils.py         # 🔧 LLM-Hilfsfunktionen
├── scripts/                 # 🛠️ Entwicklungs- und Test-Skripte
│   ├── README.md            # 📖 Skript-Dokumentation
│   ├── test_motivation.py   # 🧪 Test-Motivationsschreiben
│   ├── test_docx_generation.py  # 📄 Test-DOCX-Generierung
│   ├── debug_extraction.py  # 🔍 Debug Job-Extraktion
│   ├── create_full_test.py  # 📋 Vollständiger Test
│   ├── analyze_template.py  # 🔍 Template-Analyse
│   └── update_personal_info.py  # 👤 Persönliche Daten aktualisieren
├── templates/
│   └── template.pdf         # 📄 PDF-Vorlage
├── output/                  # 📁 Generierte PDFs und DOCX-Dateien
│   └── .gitkeep             # 📌 Ordner-Marker für Git
├── docs/                    # 📚 Dokumentation
│   └── testing_README.md    # 📖 Test-Dokumentation
└── testing/                 # 🧪 Tests und Debugging
    ├── debug_html_extraction.py
    ├── debug_llm_extraction.py
    ├── debug_llm_parsing.py
    ├── run_all_tests.py
    └── test_datalynx_specific.py
```

## 🎛️ Konfigurationsoptionen

### Verfügbare LLM-Modelle

#### OpenRouter
- `anthropic/claude-3.5-haiku` (empfohlen, schnell)
- `anthropic/claude-3.5-sonnet` (ausgewogen)
- `anthropic/claude-3-opus` (beste Qualität)
- `openai/gpt-4-turbo`
- `openai/gpt-4`
- `openai/gpt-3.5-turbo`

#### OpenAI
- `gpt-4-turbo` (beste Qualität)
- `gpt-4`
- `gpt-3.5-turbo` (schnell, kostengünstig)
- `gpt-3.5-turbo-instruct`

### Logging-Level
```properties
LOG_LEVEL=INFO    # DEBUG, INFO, WARNING, ERROR
```

### Temperatur (Kreativität)
```properties
OPENAI_TEMPERATURE=0.7    # 0.0 (deterministisch) bis 1.0 (kreativ)
```

## 🔍 Debugging

### Entwicklermodus aktivieren
```bash
# Detailliertes Logging
export LOG_LEVEL=DEBUG

# Oder in der .env Datei:
LOG_LEVEL=DEBUG
```

### Häufige Probleme

#### 1. API-Key Fehler
```
❌ Fehler: Invalid API key
```
**Lösung:** Überprüfen Sie Ihren API-Key in der `.env` Datei

#### 2. Netzwerk-Timeout
```
❌ Fehler: Request timeout
```
**Lösung:** Prüfen Sie Ihre Internetverbindung und versuchen Sie es erneut

#### 3. PDF-Generierung fehlgeschlagen
```
❌ Fehler bei PDF-Erstellung
```
**Lösung:** Überprüfen Sie die Schreibberechtigung im `output/` Ordner

#### 4. DOCX-Generierung fehlgeschlagen
```
❌ Fehler bei DOCX-Erstellung
```
**Lösung:** Stellen Sie sicher, dass `python-docx` installiert ist: `pip install python-docx`

### Test-Skripte

```bash
# Test-Motivationsschreiben erstellen
python scripts/test_motivation.py

# DOCX-Generierung testen
python scripts/test_docx_generation.py

# Job-Extraktion debuggen
python scripts/debug_extraction.py

# Vollständigen Test durchführen
python scripts/create_full_test.py

# Template analysieren
python scripts/analyze_template.py

# Persönliche Daten aktualisieren
python scripts/update_personal_info.py

# Alle Tests ausführen
python testing/run_all_tests.py
```

## 📊 Erweiterte Funktionen

### 1. Eigene PDF-Vorlage verwenden
1. Erstellen Sie eine PDF-Vorlage in `templates/`
2. Passen Sie den Pfad in der Konfiguration an

### 2. Batch-Verarbeitung
```python
# scripts/batch_processing.py
from src.job_extractor import JobExtractor
from src.ai_generator import AIGenerator
from src.template_pdf_generator import TemplateBasedPDFGenerator
from src.docx_generator import DocxGenerator

# Mehrere URLs verarbeiten
urls = [
    "https://example.com/job1",
    "https://example.com/job2",
    "https://example.com/job3"
]

extractor = JobExtractor()
ai_generator = AIGenerator()
pdf_generator = TemplateBasedPDFGenerator("templates/template.pdf")
docx_generator = DocxGenerator()

for url in urls:
    job_info = extractor.extract_from_url(url)
    motivation_letter = ai_generator.generate_motivation_letter(job_info)
    
    # Beide Formate erstellen
    pdf_path = pdf_generator.create_pdf(motivation_letter)
    docx_path = docx_generator.create_docx(motivation_letter)
    
    print(f"✅ PDF erstellt: {pdf_path}")
    print(f"✅ DOCX erstellt: {docx_path}")
```

### 3. Eigene Prompts
Passen Sie die Prompts in `src/ai_generator.py` an Ihre Bedürfnisse an.

## 🤝 Beitragen

1. Fork des Repositories
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📜 Lizenz

Dieses Projekt ist unter der MIT Lizenz veröffentlicht. Details finden Sie in der [LICENSE](LICENSE) Datei.

## 🆘 Support

- 📧 **E-Mail:** support@automi.example.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/IhrUsername/AutoMoti/issues)
- 📚 **Wiki:** [GitHub Wiki](https://github.com/IhrUsername/AutoMoti/wiki)

## 🎯 Roadmap

- [ ] **Web-Interface** - Browser-basierte Benutzeroberfläche
- [ ] **Mehrsprachigkeit** - Unterstützung für Englisch, Französisch
- [ ] **CV-Integration** - Automatische Lebenslauf-Anpassung
- [ ] **Company Research** - Automatische Firmenrecherche
- [ ] **A/B Testing** - Verschiedene Schreibstile testen
- [ ] **Analytics** - Erfolgsmetriken und Optimierungen

## 🙏 Danksagungen

- [OpenAI](https://openai.com/) für die GPT-Modelle
- [OpenRouter](https://openrouter.ai/) für den Zugang zu verschiedenen LLMs
- [LangChain](https://python.langchain.com/) für das LLM-Framework
- [Rich](https://rich.readthedocs.io/) für die schöne Konsolen-UI
- [ReportLab](https://www.reportlab.com/) für die PDF-Generierung

---

**AutoMoti** - Automatisierte Bewerbungen für die moderne Arbeitswelt 🚀
