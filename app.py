#!/usr/bin/env python3
"""
AutoMoti - Automatische Motivationsschreiben-Generierung
"""

import sys
import os
import logging
from urllib.parse import urlparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.rule import Rule
from config.config import Config
from src.job_extractor import JobExtractor
from src.ai_generator import AIGenerator
from src.pdf_generator import PDFGenerator
from src.template_pdf_generator import TemplateBasedPDFGenerator
from src.docx_generator import DocxGenerator
from src.llm_utils import LLMFactory

# Rich Console initialisieren
console = Console()

# Logging konfigurieren
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_welcome():
    """Zeigt Willkommensnachricht mit Rich Panel"""
    welcome_text = Text()
    welcome_text.append("🚀  AutoMoti\n", style="bold blue")
    welcome_text.append("Automatische Motivationsschreiben-Generierung", style="bold")
    
    console.print(Panel(
        welcome_text,
        title="[bold green]Willkommen[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))

def print_llm_info():
    """Zeigt LLM-Informationen mit Rich Panel"""
    config = Config.get_llm_config()
    
    info_text = Text()
    info_text.append(f"📡 Provider: ", style="bold")
    info_text.append(f"{config['provider'].upper()}\n", style="cyan")
    info_text.append(f"🤖 Modell: ", style="bold")
    info_text.append(f"{config['model']}\n", style="yellow")
    
    if config['provider'] == 'openrouter':
        info_text.append("💡 OpenRouter ermöglicht Zugang zu verschiedenen KI-Modellen", style="dim")
    else:
        info_text.append("💡 OpenAI GPT-Modelle werden verwendet", style="dim")
    
    console.print(Panel(
        info_text,
        title="[bold blue]LLM-Konfiguration[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))

def get_user_input():
    """Holt Benutzereingaben mit Rich Interface"""
    console.print(Panel(
        "📋  Bitte geben Sie die folgenden Informationen ein:",
        title="[bold green]Eingabe erforderlich[/bold green]",
        border_style="green"
    ))
    
    # Job-URL
    while True:
        job_url = Prompt.ask("🔗 [bold]Job-URL[/bold]").strip()
        if job_url:
            # Einfache URL-Validierung
            parsed = urlparse(job_url)
            if parsed.scheme and parsed.netloc:
                break
            else:
                console.print("❌ [red]Ungültige URL. Bitte versuchen Sie es erneut.[/red]")
        else:
            console.print("❌ [red]URL ist erforderlich. Bitte versuchen Sie es erneut.[/red]")
    
    # Persönliche Informationen aus Config laden
    personal_info = Config.get_personal_info()
    
    # Erstelle Tabelle für persönliche Informationen
    info_table = Table(show_header=True, header_style="bold magenta")
    info_table.add_column("Feld", style="cyan")
    info_table.add_column("Wert", style="white")
    
    info_table.add_row("Name", personal_info['name'])
    info_table.add_row("Adresse", personal_info['address'])
    info_table.add_row("Telefon", personal_info['phone'])
    info_table.add_row("E-Mail", personal_info['email'])
    info_table.add_row("GitHub", personal_info['github'])
    info_table.add_row("LinkedIn", personal_info['linkedin'])
    info_table.add_row("Erfahrung", personal_info['experience'])
    info_table.add_row("Fähigkeiten", personal_info['skills'])
    
    console.print(Panel(
        info_table,
        title="[bold blue]👤  Persönliche Informationen (aus .env geladen)[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))
    
    # Möglichkeit zum Überschreiben
    modify = Confirm.ask("✏️  Möchten Sie diese Informationen ändern?", default=False)
    
    if modify:
        console.print(Panel(
            "📝 Geben Sie neue Werte ein (Enter = behalten):",
            title="[bold yellow]Informationen bearbeiten[/bold yellow]",
            border_style="yellow"
        ))
        
        name = Prompt.ask(f"Name", default=personal_info['name'])
        personal_info['name'] = name
            
        address = Prompt.ask(f"Adresse", default=personal_info['address'])
        personal_info['address'] = address
            
        phone = Prompt.ask(f"Telefon", default=personal_info['phone'])
        personal_info['phone'] = phone
            
        email = Prompt.ask(f"E-Mail", default=personal_info['email'])
        personal_info['email'] = email
            
        experience = Prompt.ask(f"Berufserfahrung", default=personal_info['experience'])
        personal_info['experience'] = experience
            
        skills = Prompt.ask(f"Fähigkeiten", default=personal_info['skills'])
        personal_info['skills'] = skills
    
    return job_url, personal_info

def show_model_selection():
    """Zeigt Modellauswahl mit Rich Interface"""
    available_models = LLMFactory.get_available_models()
    config = Config.get_llm_config()
    
    # Erstelle Tabelle für verfügbare Modelle
    model_table = Table(show_header=True, header_style="bold magenta")
    model_table.add_column("Nr.", style="cyan", width=4)
    model_table.add_column("Modell", style="white")
    model_table.add_column("Provider", style="yellow")
    model_table.add_column("Status", style="green")
    
    all_models = []
    for provider, models in available_models.items():
        if (provider == 'openrouter' and Config.OPENROUTER_API_KEY) or \
           (provider == 'openai' and Config.OPENAI_API_KEY):
            for model in models:
                all_models.append((provider, model))
                status = "✅ Verfügbar" if model == config['model'] else "⚪ Verfügbar"
                model_table.add_row(str(len(all_models)), model, provider, status)
    
    model_table.add_row(str(len(all_models) + 1), "Aktuelles Modell beibehalten", "current", "🔄 Aktuell")
    
    console.print(Panel(
        model_table,
        title=f"[bold blue]🎛️ Modellauswahl (Aktuell: {config['model']})[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))
    
    try:
        choice = Prompt.ask(
            f"Wählen Sie ein Modell", 
            choices=[str(i) for i in range(1, len(all_models) + 2)],
            default=str(len(all_models) + 1)
        )
        
        choice_num = int(choice)
        if 1 <= choice_num <= len(all_models):
            provider, model = all_models[choice_num - 1]
            console.print(f"✅ [green]Gewähltes Modell: {model} ({provider})[/green]")
            return provider, model
    except (ValueError, IndexError):
        pass
    
    return None, None

def main():
    """Hauptfunktion mit Rich Interface"""
    try:
        print_welcome()
        print_llm_info()
        
        # Modellauswahl
        provider, model = show_model_selection()
        
        # Benutzereingaben
        job_url, personal_info = get_user_input()
        
        # Verarbeitung starten
        console.print(Rule("[bold green]🔄  Verarbeitung startet[/bold green]"))
        
        # 1. Job-Informationen extrahieren
        with console.status("[bold blue]1️⃣  Extrahiere Job-Informationen...[/bold blue]"):
            job_extractor = JobExtractor()
            job_description = job_extractor.extract_from_url(job_url)
        
        console.print(Panel(
            f"✅  [green]Job extrahiert:[/green] {job_description.company} - {job_description.position}",
            title="[bold green]✅  Job-Extraktion erfolgreich[/bold green]",
            border_style="green"
        ))
        
        # 2. Motivationsschreiben generieren
        with console.status("[bold blue]2️⃣  Generiere Motivationsschreiben...[/bold blue]"):
            ai_generator = AIGenerator()
            
            # Spezifisches Modell verwenden, falls ausgewählt
            if provider and model:
                ai_generator.llm = LLMFactory.create_llm(provider, model)
            
            motivation_letter = ai_generator.generate_motivation_letter(job_description, personal_info)
        
        model_info = f" mit {model} ({provider})" if provider and model else ""
        console.print(Panel(
            f"✅  [green]Motivationsschreiben generiert{model_info}[/green]",
            title="[bold green]✅  AI-Generierung erfolgreich[/bold green]",
            border_style="green"
        ))
        
        # 3. PDF & DOCX erstellen
        with console.status("[bold blue]3️⃣  Erstelle PDF und DOCX...[/bold blue]"):
            # Template-basierte PDF-Erstellung verwenden
            pdf_generator = TemplateBasedPDFGenerator("templates/template.pdf")
            
            # Template-Info anzeigen
            template_info = pdf_generator.get_template_info()
            
            pdf_path = pdf_generator.create_pdf(motivation_letter)
            
            # DOCX-Generierung hinzufügen
            docx_generator = DocxGenerator()
            docx_path = docx_generator.create_docx(motivation_letter)
        
        pdf_info = Text()
        pdf_info.append("✅  PDF erstellt: ", style="green")
        pdf_info.append(pdf_path, style="bold blue")
        pdf_info.append("\n✅  DOCX erstellt: ", style="green")
        pdf_info.append(docx_path, style="bold blue")
        
        if template_info["template_found"]:
            pdf_info.append(f"\n📄  Template: {template_info['pages']} Seiten", style="dim")
            pdf_info.append(f"\n🎨  Layout: Template-basiert", style="dim")
        else:
            pdf_info.append(f"\n📄  Layout: Standard", style="dim")
        
        console.print(Panel(
            pdf_info,
            title="[bold green]✅  PDF & DOCX-Erstellung erfolgreich[/bold green]",
            border_style="green"
        ))
        
        # 4. Zusammenfassung
        console.print(Rule("[bold green]🎉 FERTIG![/bold green]"))
        
        # Erstelle Zusammenfassungs-Tabelle
        summary_table = Table(show_header=True, header_style="bold magenta")
        summary_table.add_column("Detail", style="cyan")
        summary_table.add_column("Wert", style="white")
        
        summary_table.add_row("📄  PDF-Datei", pdf_path)
        summary_table.add_row("📄  DOCX-Datei", docx_path)
        summary_table.add_row("🏢  Unternehmen", job_description.company)
        summary_table.add_row("💼  Position", job_description.position)
        summary_table.add_row("👤  Bewerber", personal_info['name'])
        
        # Kosten anzeigen (wenn verfügbar)
        if provider and model:
            estimated_cost = LLMFactory.estimate_cost(provider, model, 1000, 500)
            if estimated_cost > 0:
                summary_table.add_row("💰 Geschätzte Kosten", f"${estimated_cost:.4f}")
        
        console.print(Panel(
            summary_table,
            title="[bold green]📊  Zusammenfassung[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
        
        console.print(Panel(
            "✨ [bold green]Motivationsschreiben erfolgreich erstellt![/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
        
    except KeyboardInterrupt:
        console.print("\n❌ [red]Vorgang abgebrochen.[/red]")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fehler in main(): {e}")
        console.print(Panel(
            f"❌ [red]Fehler: {e}[/red]",
            title="[bold red]❌ Fehler aufgetreten[/bold red]",
            border_style="red"
        ))
        sys.exit(1)

if __name__ == "__main__":
    main()