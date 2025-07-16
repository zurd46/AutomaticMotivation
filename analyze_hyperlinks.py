#!/usr/bin/env python3
"""
Analyse-Tool für DOCX und PDF Hyperlinks
"""

import zipfile
import re
import os

def analyze_docx(docx_path):
    """Analysiert DOCX-Datei auf Hyperlinks"""
    if not os.path.exists(docx_path):
        print(f"DOCX-Datei nicht gefunden: {docx_path}")
        return
    
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        # Relationships prüfen
        print('=== DOCX Relationships ===')
        try:
            rels_xml = zip_ref.read('word/_rels/document.xml.rels')
            rels_content = rels_xml.decode('utf-8')
            print(rels_content)
            
            # Hyperlinks aus Relationships extrahieren
            hyperlink_pattern = r'<Relationship[^>]*Type="[^"]*hyperlink[^"]*"[^>]*Target="([^"]+)"'
            hyperlink_matches = re.findall(hyperlink_pattern, rels_content)
            print(f'\nGefundene Hyperlink-Ziele: {hyperlink_matches}')
            
        except Exception as e:
            print(f'Fehler beim Lesen der Relationships: {e}')
        
        # Document XML analysieren
        print('\n=== DOCX Document Analysis ===')
        try:
            doc_xml = zip_ref.read('word/document.xml')
            doc_content = doc_xml.decode('utf-8')
            
            # Hyperlinks im Document finden
            hyperlink_pattern = r'<w:hyperlink[^>]*r:id="([^"]+)"[^>]*>(.*?)</w:hyperlink>'
            hyperlinks = re.findall(hyperlink_pattern, doc_content, re.DOTALL)
            print(f'Anzahl Hyperlinks im Document: {len(hyperlinks)}')
            
            for i, (rid, content) in enumerate(hyperlinks):
                print(f'\nHyperlink {i+1}:')
                print(f'  Relation ID: {rid}')
                # Text aus dem Hyperlink extrahieren
                text_pattern = r'<w:t[^>]*>([^<]+)</w:t>'
                text_matches = re.findall(text_pattern, content)
                print(f'  Text: {" ".join(text_matches)}')
                
            # Nach GitHub-Erwähnungen suchen
            github_mentions = re.findall(r'github[^<]*', doc_content, re.IGNORECASE)
            print(f'\nGitHub-Erwähnungen im Text: {len(github_mentions)}')
            for mention in github_mentions:
                print(f'  - {mention}')
                
            # Nach Projekt-Namen suchen
            project_mentions = re.findall(r'(ZurdLLMWS|AutomaticMotivation|Auto-search-jobs)', doc_content)
            print(f'\nProjekt-Namen im Text: {project_mentions}')
            
            # Nach dem generierten Text suchen
            print('\n=== Vollständiger Text-Inhalt (erste 2000 Zeichen) ===')
            text_content = re.sub(r'<[^>]+>', '', doc_content)
            print(text_content[:2000])
            
        except Exception as e:
            print(f'Fehler beim Lesen des Document XML: {e}')

def analyze_pdf(pdf_path):
    """Analysiert PDF-Datei auf Hyperlinks"""
    if not os.path.exists(pdf_path):
        print(f"PDF-Datei nicht gefunden: {pdf_path}")
        return
    
    print('\n=== PDF Analysis ===')
    try:
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read().decode('latin-1', errors='ignore')
            
        # Nach Hyperlinks suchen
        hyperlink_pattern = r'/URI\s*\([^)]+\)'
        hyperlinks = re.findall(hyperlink_pattern, pdf_content)
        print(f'Anzahl Hyperlinks im PDF: {len(hyperlinks)}')
        
        for i, link in enumerate(hyperlinks):
            print(f'  Hyperlink {i+1}: {link}')
            
        # Nach GitHub-Erwähnungen suchen
        github_mentions = re.findall(r'github[^)]*', pdf_content, re.IGNORECASE)
        print(f'\nGitHub-Erwähnungen im PDF: {len(github_mentions)}')
        for mention in github_mentions:
            print(f'  - {mention}')
            
    except Exception as e:
        print(f'Fehler beim Lesen des PDF: {e}')

if __name__ == "__main__":
    # Analysiere beide Dateien
    docx_path = 'output/Motivationsschreiben_Rocken_Partner_Energieversorger_in_der_Zentralschweiz_160725.docx'
    pdf_path = 'output/Motivationsschreiben_Rocken®_Partner_(Energieversorger_in_der_Zentralschweiz)_160725.pdf'
    
    analyze_docx(docx_path)
    analyze_pdf(pdf_path)
