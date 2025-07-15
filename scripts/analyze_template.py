#!/usr/bin/env python3
"""
Template-Analyse-Tool für AutoMoti
"""

import os
import sys
from src.pdf_generator import PDFGenerator

def analyze_template():
    """Analysiert das PDF-Template und zeigt die Ergebnisse"""
    template_path = "templates/template.pdf"
    
    print("=" * 60)
    print("🔍 Template-Analyse")
    print("=" * 60)
    
    if not os.path.exists(template_path):
        print(f"❌ Template nicht gefunden: {template_path}")
        return
    
    try:
        pdf_generator = PDFGenerator(template_path=template_path)
        analysis = pdf_generator.analyze_template(template_path)
        
        print(f"📄 Template-Datei: {template_path}")
        print(f"📊 Status: {'✅ Gefunden' if analysis.get('template_found') else '❌ Nicht gefunden'}")
        
        if analysis.get('template_found'):
            print(f"📃 Seiten: {analysis.get('pages', 0)}")
            
            # Text-Inhalt anzeigen (erste 300 Zeichen)
            text_content = analysis.get('text_content', '')
            if text_content:
                print(f"📝 Text-Inhalt (Auszug):")
                print("-" * 40)
                print(text_content[:300])
                if len(text_content) > 300:
                    print("... (gekürzt)")
                print("-" * 40)
            
            # Layout-Informationen
            layout = analysis.get('layout', {})
            if layout:
                print(f"📏 Layout-Informationen:")
                for page_key, page_info in layout.items():
                    print(f"  • {page_key}: {page_info.get('width', 0):.1f} x {page_info.get('height', 0):.1f} pt")
        
        print("\n" + "=" * 60)
        print("✅ Template-Analyse abgeschlossen")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Fehler bei Template-Analyse: {e}")

if __name__ == "__main__":
    analyze_template()
