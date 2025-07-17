#!/usr/bin/env python3
"""
Test der intelligenten Stellenanalyse mit echten IT-Support-Daten
"""

import sys
sys.path.append('.')

from src.intelligent_job_analyzer import IntelligentJobAnalyzer

def test_real_it_support():
    analyzer = IntelligentJobAnalyzer()
    
    # Echte IT-Support-Daten aus dem Luzerner Kantonsspital
    position = "ICT Supporterin/ICT Supporter"
    description = "ICT Support im Spitalumfeld mit komplexen IT-Aufgaben wie Installation und Wartung von Arbeitsplatzsystemen, Peripheriegeräten und Software. Verantwortlich für Troubleshooting, Kundenservice und Betreuung von Lernenden."
    requirements = "Abgeschlossene Informatikausbildung, Mehrjährige Supporterfahrung, ITIL-Zertifizierung von Vorteil, Analytische Fähigkeiten und strukturierte Herangehensweise, Proaktive Einstellung und Servicegedanken, Sehr gute Deutschkenntnisse, Hands-on Mentalität, Flexibilität und Kreativität"
    
    result = analyzer.analyze_job(position, description, requirements)
    
    print("=== Test mit echten IT-Support-Daten ===")
    print(f"Position: {position}")
    print(f"Kategorie: {result['category'].value}")
    print(f"Confidence: {result['analysis_confidence']:.2f}")
    print(f"Schlüsselanforderungen: {result['key_requirements']}")
    print(f"Relevante Fähigkeiten: {result['relevant_skills']}")
    print(f"Hauptaufgaben: {result['main_tasks']}")
    print(f"Fokus-Empfehlungen: {result['focus_recommendations']['focus_areas']}")
    print(f"Zu vermeiden: {result['focus_recommendations']['avoid_areas']}")
    print(f"Schlüsselphrasen: {result['focus_recommendations']['key_phrases']}")
    print(f"Erfahrungs-Betonung: {result['focus_recommendations']['experience_emphasis']}")

if __name__ == "__main__":
    test_real_it_support()
