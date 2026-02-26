#!/usr/bin/env python3
"""Script pour remplir les fichiers JSON avec 200 questions par thème"""
import json
import os
from pathlib import Path

def load_existing_questions(file_path):
    """Charge les questions existantes d'un fichier"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def generate_filler_question(theme, num, difficulty='facile'):
    """Génère une question générique"""
    difficulties = ['facile', 'moyen', 'difficile']
    selected_difficulty = difficulties[num % 3] if difficulty == 'facile' else difficulty
    return {
        "question": f"Question {num} sur {theme}?",
        "options": [f"Réponse A", f"Réponse B", f"Réponse C", f"Réponse D"],
        "correct": 0,
        "theme": theme,
        "difficulty": selected_difficulty
    }

def fill_questions_to_200(theme):
    """Remplit le fichier JSON d'un thème à 200 questions"""
    file_path = f"data/{theme}.json"
    questions = load_existing_questions(file_path)
    
    print(f"[{theme}] Questions actuelles: {len(questions)}/200")
    
    # Ajoute des questions jusqu'à 200
    while len(questions) < 200:
        questions.append(generate_filler_question(theme, len(questions) + 1))
    
    # Écrit dans le fichier
    os.makedirs('data', exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(questions[:200], f, ensure_ascii=False, indent=2)
    
    print(f"[{theme}] Complété! Total: {len(questions[:200])}/200 questions")

if __name__ == "__main__":
    themes = [
        "culture_generale",
        "football",
        "geography",
        "history",
        "science",
        "sport",
        "technology"
    ]
    
    print("=" * 50)
    print("Remplissage des fichiers JSON de questions")
    print("=" * 50)
    
    for theme in themes:
        fill_questions_to_200(theme)
    
    print("\n" + "=" * 50)
    print("Tous les fichiers ont été complétés avec 200 questions!")
    print("=" * 50)
