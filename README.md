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
├── config/config.py                 # Konfiguration
├── src/
│   ├── ai_generator.py              # KI-Generierung
│   ├── github_project_extractor.py  # GitHub-Integration
│   ├── job_extractor.py             # Stellenanalyse
│   ├── pdf_generator.py             # PDF-Erstellung
│   └── docx_generator.py            # DOCX-Erstellung
└── output/                          # Generierte Dokumente
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