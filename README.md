# 🚀 AutomaticMotivation

KI-gestütztes System zur automatischen Generierung von personalisierten Motivationsschreiben mit GitHub-Integration und intelligenter Stellenanalyse.

## ✨ Features

- 🎯 **GitHub-Integration** - Automatische Auswahl relevanter Projekte
- 📊 **Konkrete Kennzahlen** - Realistische Erfolgskennzahlen basierend auf Projekttyp
- 🤖 **Multi-LLM-Support** - OpenAI GPT-4, Claude 3.5 Haiku/Sonnet
- 📄 **Dual-Format** - PDF und DOCX gleichzeitig
- 🔍 **Stellenanalyse** - Automatische Extraktion von Jobanforderungen

## 🔧 Installation

```bash
git clone https://github.com/zurd46/AutomaticMotivation.git
cd AutomaticMotivation
pip install -r requirements.txt
```

## ⚙️ Konfiguration

Erstellen Sie eine `.env` Datei:

```properties
# GitHub-Integration
PERSONAL_GITHUB=https://github.com/IhrUsername

# Persönliche Informationen
PERSONAL_NAME=Ihr Name
PERSONAL_EMAIL=ihr@email.com
PERSONAL_PHONE=+41 XX XXX XX XX
PERSONAL_SKILLS=Python, KI, Webentwicklung, etc.

# API-Konfiguration (OpenRouter empfohlen)
OPENROUTER_API_KEY=sk-or-v1-ihr-api-key
OPENROUTER_MODEL=anthropic/claude-3.5-haiku

# Fallback: OpenAI
OPENAI_API_KEY=sk-proj-ihr-openai-api-key
```

## 🚀 Verwendung

```bash
python app.py
```

1. KI-Modell auswählen
2. Stellenausschreibung-URL eingeben
3. System analysiert Job und GitHub-Projekte
4. Generiert personalisierte Bewerbung (PDF + DOCX)

## 🛠️ Tests

```bash
# GitHub-Integration testen
python test_github_projects.py

# Spezifitäts-Analyse
python test_ultra_specific.py

# Vollständige Bewerbung
python test_improved_ai.py
```

## 📁 Projektstruktur

```
AutomaticMotivation/
├── app.py                           # Hauptanwendung
├── requirements.txt                 # Abhängigkeiten
├── .env                            # Konfigurationsdatei
├── .env.example                    # Beispiel-Konfiguration
├── .gitignore                      # Git-Ignore-Regeln
├── .gitattributes                  # Git-Attribute
├── README.md                       # Dokumentation
├── config/
│   ├── config.py                   # Konfigurationsverwaltung
│   └── __pycache__/               # Python-Cache
├── src/
│   ├── __init__.py                # Python-Paket-Initialisierung
│   ├── ai_generator.py            # KI-Generierung
│   ├── docx_generator.py          # DOCX-Erstellung
│   ├── github_project_extractor.py # GitHub-Integration
│   ├── job_extractor.py           # Stellenanalyse
│   ├── llm_utils.py               # LLM-Hilfsfunktionen
│   ├── models.py                  # Datenmodelle
│   ├── pdf_generator.py           # PDF-Erstellung
│   ├── template_pdf_generator.py  # Template-PDF-Erstellung
│   └── __pycache__/               # Python-Cache
├── templates/
│   └── template.pdf               # PDF-Vorlage
├── output/
│   ├── .gitkeep                   # Git-Placeholder
│   └── [Generierte Dokumente]     # PDF/DOCX-Ausgaben
├── testing/
│   ├── debug_html_extraction.py   # HTML-Extraktion debuggen
│   ├── debug_llm_extraction.py    # LLM-Extraktion debuggen
│   ├── debug_llm_parsing.py       # LLM-Parsing debuggen
│   ├── run_all_tests.py           # Alle Tests ausführen
│   └── test_datalynx_specific.py  # Spezifische Tests
├── scripts/
│   ├── analyze_template.py        # Template-Analyse
│   ├── create_full_test.py        # Vollständige Tests erstellen
│   ├── debug_extraction.py        # Extraktion debuggen
│   ├── README.md                  # Script-Dokumentation
│   ├── test_beei_docx.py          # DOCX-Tests
│   ├── test_docx_fix.py           # DOCX-Korrekturen testen
│   ├── test_docx_generation.py    # DOCX-Generierung testen
│   ├── test_github_projects.py    # GitHub-Integration testen
│   ├── test_improved_ai.py        # Verbesserte KI-Tests
│   ├── test_motivation.py         # Motivationsschreiben testen
│   ├── test_ultra_specific.py     # Spezifitäts-Tests
│   └── update_personal_info.py    # Persönliche Infos aktualisieren
└── docs/
    ├── cleanup_summary.md         # Bereinigungsübersicht
    ├── docx_feature_summary.md    # DOCX-Feature-Übersicht
    └── testing_README.md          # Test-Dokumentation
```

## 🔍 Problemlösung

**GitHub-Projekte nicht gefunden?**
- Überprüfen Sie `PERSONAL_GITHUB` in `.env`
- Stellen Sie sicher, dass Repositories öffentlich sind

**Niedrige Spezifitäts-Score?**
- Verbessern Sie GitHub-Projekt-Beschreibungen
- Fügen Sie relevante Topics hinzu

**API-Limits?**
- Wechseln Sie zu OpenRouter für höhere Limits

## 📜 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.