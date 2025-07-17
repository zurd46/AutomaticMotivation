#!/usr/bin/env python3
"""
Test der dynamischen GitHub-Projekt-Pattern-Erkennung
"""

import re
from config.config import Config

def test_dynamic_patterns():
    # Test der dynamischen Pattern-Erkennung
    project_urls = Config.get_github_project_urls()
    print(f'Verfügbare Projekte: {len(project_urls)}')
    for name, url in list(project_urls.items())[:5]:  # Zeige erste 5
        print(f'  {name}: {url}')
    
    # Erstelle dynamisches Pattern
    escaped_projects = [re.escape(project) for project in project_urls.keys()]
    github_project_pattern = f"({'|'.join(escaped_projects)})"
    
    print(f'\nPattern (erste 200 Zeichen): {github_project_pattern[:200]}...')
    
    # Test mit Beispieltext
    test_text = 'Ich habe an AutomaticMotivation, ZurdLLMWS und ZurdSynthDataGen gearbeitet.'
    matches = re.findall(github_project_pattern, test_text)
    print(f'\nTest-Text: {test_text}')
    print(f'Gefundene Matches: {matches}')
    
    # Test mit verschiedenen Projektnamen
    test_cases = [
        'AutomaticMotivation',
        'ZurdLLMWS',
        'ZurdSynthDataGen',
        'python-ftp-data-uploader',
        'Auto-search-jobs-to-Email'
    ]
    
    print('\nEinzelne Tests:')
    for project in test_cases:
        matches = re.findall(github_project_pattern, f'Das Projekt {project} ist interessant.')
        print(f'  {project}: {matches}')

if __name__ == "__main__":
    test_dynamic_patterns()
