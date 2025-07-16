# 🚀 AutomaticMotivation

KI-gestütztes System zur automatischen Generierung von personalisierten Motivationsschreiben mit GitHub-Integration, LinkedIn-Profil-Extraktion und intelligenter Stellenanalyse.

## ✨ Features

- 🎯 **GitHub-Integration** - Automatische Auswahl relevanter Projekte mit direkten Hyperlinks
- � **LinkedIn-Integration** - Echte Profildaten-Extraktion und Verlinkung
- �📊 **Konkrete Kennzahlen** - Realistische Erfolgskennzahlen basierend auf Projekttyp
- 🤖 **Multi-LLM-Support** - OpenAI GPT-4, Claude 3.5 Haiku/Sonnet, Llama 2
- 📄 **Dual-Format** - PDF und DOCX mit funktionierenden Hyperlinks
- 🔍 **Stellenanalyse** - Automatische Extraktion von Jobanforderungen
- 🎨 **Template-System** - PDF-Vorlagen für professionelles Layout
- 💡 **Intelligente Verlinkung** - Automatische Hyperlinks für GitHub-Projekte und LinkedIn-Profil

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

# LinkedIn-Integration
PERSONAL_LINKEDIN=https://www.linkedin.com/in/ihr-profil

# Persönliche Informationen
PERSONAL_NAME=Ihr Name
PERSONAL_EMAIL=ihr@email.com
PERSONAL_PHONE=+41 XX XXX XX XX
PERSONAL_ADDRESS=Ihre Adresse
PERSONAL_EXPERIENCE=X+ Jahre Berufserfahrung
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

1. KI-Modell auswählen (15 verfügbare Modelle)
2. Stellenausschreibung-URL eingeben
3. System analysiert Job, GitHub-Projekte und LinkedIn-Profil
4. Generiert personalisierte Bewerbung (PDF + DOCX) mit funktionierenden Hyperlinks

## 🔗 Hyperlink-Features

- **GitHub-Projekte** werden automatisch verlinkt (z.B. "ZurdLLMWS" → GitHub-Repository)
- **LinkedIn-Profil** wird verlinkt ohne URL-Anzeige im Text
- **Funktioniert in PDF und DOCX** - Alle Links sind klickbar
- **Automatische Erkennung** - Keine manuelle Formatierung erforderlich

## � LinkedIn-Integration

- **Echte Datenextraktion** - Kein Mock-Content, echte Profildaten
- **Automatische Verlinkung** - "LinkedIn-Profil" wird automatisch verlinkt
- **Fallback-System** - Bei Extraktion-Fehlern werden Config-Daten verwendet
- **Skills-Matching** - LinkedIn-Skills werden passend zur Stelle integriert

## �🛠️ Tests

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
│   ├── docx_generator.py          # DOCX-Erstellung mit Hyperlinks
│   ├── github_project_extractor.py # GitHub-Integration
│   ├── job_extractor.py           # Stellenanalyse
│   ├── linkedin_extractor.py      # LinkedIn-Profil-Extraktion
│   ├── llm_utils.py               # LLM-Hilfsfunktionen
│   ├── models.py                  # Datenmodelle
│   ├── pdf_generator.py           # PDF-Erstellung
│   ├── template_pdf_generator.py  # Template-PDF-Erstellung mit Hyperlinks
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

### GitHub-Integration nicht funktioniert?
- Überprüfen Sie die `PERSONAL_GITHUB` URL in der `.env` Datei
- Stellen Sie sicher, dass Ihre GitHub-Repositories öffentlich sind
- Testen Sie mit `python test_github_projects.py`

### LinkedIn-Extraktion schlägt fehl?
- LinkedIn blockiert möglicherweise den Zugriff (429 Error)
- System verwendet automatisch Fallback-Daten aus der Config
- Überprüfen Sie die `PERSONAL_LINKEDIN` URL in der `.env` Datei

### Hyperlinks funktionieren nicht?
- Überprüfen Sie, ob die generierten Dateien in `output/` korrekt sind
- PDF-Hyperlinks: Testen Sie mit einem PDF-Reader, der Links unterstützt
- DOCX-Hyperlinks: Öffnen Sie die Datei in Microsoft Word

### KI-Generierung fehlgeschlagen?
- Überprüfen Sie Ihre API-Keys (`OPENROUTER_API_KEY` oder `OPENAI_API_KEY`)
- Wählen Sie ein anderes Modell aus der Liste
- Prüfen Sie Ihre Internetverbindung

## 🆕 Neueste Updates

### Version 2.0 - LinkedIn & Hyperlinks
- ✅ **LinkedIn-Integration** - Echte Profildaten-Extraktion
- ✅ **Hyperlink-System** - Funktioniert in PDF und DOCX
- ✅ **Template-PDF** - Professionelle Vorlagen
- ✅ **Multi-Model-Support** - 15 KI-Modelle verfügbar
- ✅ **Verbesserte UI** - Rich-Console-Interface

### Version 1.0 - Grundfunktionen
- ✅ **GitHub-Integration** - Automatische Projektauswahl
- ✅ **Dual-Format** - PDF + DOCX Ausgabe
- ✅ **Stellenanalyse** - Automatische Jobextraktion
- ✅ **KI-Generierung** - Personalisierte Motivationsschreiben

## 📝 Lizenz

MIT License - Siehe LICENSE Datei für Details.

## 🤝 Beiträge

Beiträge sind willkommen! Öffnen Sie ein Issue oder erstellen Sie einen Pull Request.

## 🚀 Roadmap

- [ ] **Multi-Language Support** - Englische Motivationsschreiben
- [ ] **XING-Integration** - Deutsche Business-Netzwerk-Unterstützung
- [ ] **Cover Letter Templates** - Verschiedene Vorlagen
- [ ] **Batch Processing** - Mehrere Bewerbungen gleichzeitig
- [ ] **Web Interface** - Browser-basierte Benutzeroberfläche

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