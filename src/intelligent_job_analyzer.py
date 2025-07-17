#!/usr/bin/env python3
"""
Intelligente Stellenanalyse für bessere Anforderungsextraktion
"""

import re
from typing import Dict, List, Tuple
from enum import Enum

class JobCategory(Enum):
    IT_SUPPORT = "IT_Support"
    SOFTWARE_DEVELOPMENT = "Software_Development"
    DATA_SCIENCE = "Data_Science"
    NETWORK_ADMIN = "Network_Admin"
    CYBERSECURITY = "Cybersecurity"
    PROJECT_MANAGEMENT = "Project_Management"
    BUSINESS_ANALYSIS = "Business_Analysis"
    DEVOPS = "DevOps"
    UNKNOWN = "Unknown"

class IntelligentJobAnalyzer:
    """Intelligente Analyse von Stellenausschreibungen"""
    
    def __init__(self):
        self.job_patterns = {
            JobCategory.IT_SUPPORT: {
                'keywords': [
                    'support', 'helpdesk', 'servicedesk', 'technischer support',
                    'anwendersupport', 'benutzerunterstützung', 'troubleshooting',
                    'incident', 'ticketing', 'hardware', 'installation',
                    'wartung', 'konfiguration', 'arbeitsplatz', 'enduser',
                    'first level', 'second level', 'user support', 'ict support',
                    'it support', 'supporter', 'supporterin', 'kundenservice',
                    'betreuung', 'systemadministration', 'systembetreuung',
                    'anwenderschulung', 'systemwartung', 'it-betreuung'
                ],
                'skills': [
                    'windows administration', 'active directory', 'office 365',
                    'ticketing systeme', 'remote support', 'hardware diagnose',
                    'netzwerk grundlagen', 'itil', 'service management',
                    'kundenbetreuung', 'kommunikation', 'problem solving',
                    'supporterfahrung', 'systemadministration', 'troubleshooting',
                    'servicegedanken', 'hands-on mentalität', 'analytische fähigkeiten',
                    'strukturierte herangehensweise', 'proaktive einstellung'
                ],
                'tasks': [
                    'störungen beheben', 'software installieren', 'hardware warten',
                    'benutzer schulen', 'tickets bearbeiten', 'dokumentation',
                    'remote support', 'vor-ort support', 'system konfiguration',
                    'arbeitsplatzsysteme', 'peripheriegeräte', 'systemwartung',
                    'anwenderbetreuung', 'lernende betreuen', 'kundenservice'
                ]
            },
            JobCategory.SOFTWARE_DEVELOPMENT: {
                'keywords': [
                    'entwicklung', 'programmierung', 'software engineer',
                    'developer', 'coding', 'implementation', 'full stack',
                    'frontend', 'backend', 'agile', 'scrum', 'git',
                    'continuous integration', 'testing', 'debugging'
                ],
                'skills': [
                    'programmiersprachen', 'frameworks', 'datenbanken',
                    'version control', 'testing', 'debugging', 'code review',
                    'software architecture', 'design patterns', 'apis'
                ],
                'tasks': [
                    'code entwickeln', 'features implementieren', 'bugs fixen',
                    'code reviews', 'testing', 'dokumentation schreiben',
                    'architektur design', 'deployment', 'monitoring'
                ]
            },
            JobCategory.DATA_SCIENCE: {
                'keywords': [
                    'data science', 'machine learning', 'ai', 'analytics',
                    'statistik', 'datenanalyse', 'big data', 'visualization',
                    'data scientist', 'data analyst', 'tensorflow', 'pytorch',
                    'künstliche intelligenz', 'datenwissenschaft', 'algorithmus',
                    'predictive modeling', 'deep learning', 'neural networks'
                ],
                'skills': [
                    'data analysis', 'machine learning', 'statistics',
                    'python', 'r programming', 'sql', 'visualization', 'modeling',
                    'numpy', 'pandas', 'scikit-learn', 'jupyter'
                ],
                'tasks': [
                    'daten analysieren', 'modelle entwickeln', 'berichte erstellen',
                    'datenvisualisierung', 'algorithmen implementieren',
                    'predictive analytics', 'data mining', 'statistical analysis'
                ]
            }
        }
    
    def analyze_job(self, position: str, description: str, requirements: str) -> Dict:
        """Analysiert eine Stellenausschreibung und kategorisiert sie"""
        
        # Kombiniere alle Texte für Analyse
        full_text = f"{position} {description} {requirements}".lower()
        
        # Kategorisierung
        category = self._categorize_job(full_text)
        
        # Extrahiere relevante Informationen
        key_requirements = self._extract_key_requirements(full_text, category)
        relevant_skills = self._extract_relevant_skills(full_text, category)
        main_tasks = self._extract_main_tasks(full_text, category)
        
        # Erstelle Fokus-Empfehlungen für die AI
        focus_recommendations = self._generate_focus_recommendations(category, key_requirements)
        
        return {
            'category': category,
            'key_requirements': key_requirements,
            'relevant_skills': relevant_skills,
            'main_tasks': main_tasks,
            'focus_recommendations': focus_recommendations,
            'analysis_confidence': self._calculate_confidence(full_text, category)
        }
    
    def _categorize_job(self, text: str) -> JobCategory:
        """Kategorisiert die Stelle basierend auf Schlüsselwörtern"""
        
        print(f"DEBUG: Analyzing text: {text[:200]}...")
        
        category_scores = {}
        
        for category, patterns in self.job_patterns.items():
            score = 0
            found_keywords = []
            for keyword in patterns['keywords']:
                # Verwende Word-Boundary-Matching für bessere Genauigkeit
                import re
                # Suche nach ganzen Wörtern oder Phrasen
                if len(keyword.split()) > 1:
                    # Multi-Word-Keyword
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                else:
                    # Single-Word-Keyword - nur wenn es länger als 2 Zeichen ist
                    if len(keyword) > 2:
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                    else:
                        # Für kurze Keywords wie "ai" oder "r", verwende exakte Phrase-Matching
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                
                matches = re.findall(pattern, text, re.IGNORECASE)
                count = len(matches)
                
                if count > 0:
                    # Gewichtung basierend auf Keyword-Relevanz
                    score += count * 2
                    found_keywords.append(f"{keyword}({count})")
                    
                    # Zusätzliche Gewichtung für Keyword-Häufigkeit
                    if count > 2:
                        score += 3
            
            category_scores[category] = score
            print(f"DEBUG: {category.value}: Score={score}, Keywords={found_keywords}")
        
        # Bestimme die Kategorie mit höchstem Score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            print(f"DEBUG: Best category: {best_category.value} with score {category_scores[best_category]}")
            if category_scores[best_category] > 1:  # Reduziere Mindest-Confidence
                return best_category
        
        return JobCategory.UNKNOWN
    
    def _extract_key_requirements(self, text: str, category: JobCategory) -> List[str]:
        """Extrahiert die wichtigsten Anforderungen für die Kategorie"""
        
        if category not in self.job_patterns:
            return []
        
        relevant_skills = self.job_patterns[category]['skills']
        found_requirements = []
        
        for skill in relevant_skills:
            if skill in text:
                found_requirements.append(skill)
        
        # Zusätzliche Anforderungen durch Regex-Patterns
        if category == JobCategory.IT_SUPPORT:
            # Suche nach Jahren Erfahrung
            experience_pattern = r'(\d+)\s*jahr[e]?\s*(erfahrung|berufserfahrung)'
            experience_match = re.search(experience_pattern, text)
            if experience_match:
                found_requirements.append(f"{experience_match.group(1)} Jahre Erfahrung")
            
            # Suche nach Zertifizierungen
            cert_patterns = ['itil', 'microsoft', 'cisco', 'comptia', 'zertifizierung']
            for cert in cert_patterns:
                if cert in text:
                    found_requirements.append(f"{cert} Kenntnisse")
        
        return found_requirements[:8]  # Limitiere auf 8 wichtigste
    
    def _extract_relevant_skills(self, text: str, category: JobCategory) -> List[str]:
        """Extrahiert relevante Fähigkeiten für die Kategorie"""
        
        if category not in self.job_patterns:
            return []
        
        skills = self.job_patterns[category]['skills']
        found_skills = [skill for skill in skills if skill in text]
        
        return found_skills[:10]  # Top 10 relevante Skills
    
    def _extract_main_tasks(self, text: str, category: JobCategory) -> List[str]:
        """Extrahiert Hauptaufgaben für die Kategorie"""
        
        if category not in self.job_patterns:
            return []
        
        tasks = self.job_patterns[category]['tasks']
        found_tasks = [task for task in tasks if any(word in text for word in task.split())]
        
        return found_tasks[:6]  # Top 6 Hauptaufgaben
    
    def _generate_focus_recommendations(self, category: JobCategory, requirements: List[str]) -> Dict[str, str]:
        """Generiert Fokus-Empfehlungen für die AI-Generierung"""
        
        recommendations = {
            'tone': 'professional',
            'focus_areas': [],
            'avoid_areas': [],
            'key_phrases': [],
            'experience_emphasis': ''
        }
        
        if category == JobCategory.IT_SUPPORT:
            recommendations.update({
                'focus_areas': [
                    'Kundenservice und Benutzerunterstützung',
                    'Problemlösung und Troubleshooting',
                    'Technische Kommunikation',
                    'Service-Orientierung',
                    'Systemadministration',
                    'Hardware- und Software-Support'
                ],
                'avoid_areas': [
                    'Softwareentwicklung',
                    'Programmiersprachen',
                    'Code-Entwicklung',
                    'Agile Entwicklung',
                    'Development Frameworks'
                ],
                'key_phrases': [
                    'IT-Support-Erfahrung',
                    'Anwenderbetreuung',
                    'Ticketing-Systeme',
                    'First-Level-Support',
                    'Servicedesk-Erfahrung',
                    'Problemlösung im IT-Bereich'
                ],
                'experience_emphasis': 'IT-Support, Helpdesk, Systemadministration'
            })
        
        elif category == JobCategory.SOFTWARE_DEVELOPMENT:
            recommendations.update({
                'focus_areas': [
                    'Softwareentwicklung',
                    'Programmierung',
                    'Technische Umsetzung',
                    'Code-Qualität',
                    'Agile Methoden'
                ],
                'avoid_areas': [
                    'Reine IT-Support-Tätigkeiten',
                    'Helpdesk-Aktivitäten'
                ],
                'key_phrases': [
                    'Entwicklungserfahrung',
                    'Programmiersprachen',
                    'Software-Architektur',
                    'Agile Entwicklung'
                ],
                'experience_emphasis': 'Software-Entwicklung, Programmierung'
            })
        
        return recommendations
    
    def _calculate_confidence(self, text: str, category: JobCategory) -> float:
        """Berechnet die Confidence der Kategorisierung"""
        
        if category == JobCategory.UNKNOWN:
            return 0.0
        
        total_keywords = len(self.job_patterns[category]['keywords'])
        found_keywords = sum(1 for keyword in self.job_patterns[category]['keywords'] if keyword in text)
        
        confidence = found_keywords / total_keywords
        return min(confidence, 1.0)

# Test-Funktion
def test_analyzer():
    analyzer = IntelligentJobAnalyzer()
    
    # Test IT-Support Position
    position = "ICT Supporterin/ICT Supporter"
    description = "IT-Support im Spitalumfeld mit komplexen IT-Aufgaben wie Installation und Wartung von Arbeitsplatzsystemen"
    requirements = "Abgeschlossene Informatikausbildung, Mehrjährige Supporterfahrung, ITIL-Zertifizierung von Vorteil"
    
    result = analyzer.analyze_job(position, description, requirements)
    
    print("=== Intelligente Stellenanalyse ===")
    print(f"Kategorie: {result['category'].value}")
    print(f"Confidence: {result['analysis_confidence']:.2f}")
    print(f"Schlüsselanforderungen: {result['key_requirements']}")
    print(f"Relevante Fähigkeiten: {result['relevant_skills']}")
    print(f"Hauptaufgaben: {result['main_tasks']}")
    print(f"Fokus-Empfehlungen: {result['focus_recommendations']['focus_areas']}")
    print(f"Zu vermeiden: {result['focus_recommendations']['avoid_areas']}")

if __name__ == "__main__":
    test_analyzer()
