#!/usr/bin/env python3
"""
Script pour générer 200 vraies questions par thème via l'API OpenAI (GPT)

Prérequis:
    pip install openai
    
Utilisation:
    export OPENAI_API_KEY="votre-clé-api"
    python3 generate_with_api.py
"""

import json
import os
from openai import OpenAI

# Configuration
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

THEMES = {
    "culture_generale": "culture générale (cinéma, littérature, art, histoire générale)",
    "science": "science (physique, chimie, biologie, astronomie, médecine)",
    "football": "football (clubs, joueurs, compétitions, règles, histoire du football)",
    "geography": "géographie (capitales, pays, continents, océans, montagnes, fleuves)",
    "history": "histoire (événements historiques, personnages, guerres, civilisations)",
    "sport": "sport en général (tous sports sauf football, athlètes, Jeux Olympiques)",
    "technology": "technologie (informatique, inventions, internet, programmation, hardware)"
}

def load_existing_questions(theme):
    """Charge les questions existantes"""
    file_path = f"data/{theme}.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def generate_questions_with_gpt(theme, theme_description, count=200):
    """Génère des questions via l'API OpenAI GPT"""
    
    prompt = f"""
Génère exactement {count} questions de quiz sur le thème: {theme_description}.

Format JSON requis (array d'objets):
[
  {{
    "question": "Question ici?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0,
    "theme": "{theme}",
    "difficulty": "facile"
  }}
]

Règles:
- Chaque question doit avoir exactement 4 options
- Le champ "correct" est l'index (0-3) de la bonne réponse
- Varier les difficultés: facile, moyen, difficile
- Questions variées et intéressantes
- En français
- Retourne UNIQUEMENT le JSON, sans texte avant ou après
"""
    
    print(f"\n[{theme}] Génération de {count} questions via GPT...")
    
    try:
        response = client.chat.completions.create(
            model=""gpt-5.2"4o",  # ou "gpt-3.5-turbo" pour moins cher
            messages=[
                {"role": "system", "content": "Tu es un expert en création de quiz éducatifs. Tu génères des questions de qualité avec des réponses précises."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=16000
        )
        
        content = response.choices[0].message.content
        
        # Nettoie le contenu pour extraire le JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        questions = json.loads(content.strip())
        print(f"[{theme}] ✅ {len(questions)} questions générées avec succès")
        return questions
        
    except Exception as e:
        print(f"[{theme}] ❌ Erreur: {e}")
        return []

def save_questions(theme, questions):
    """Sauvegarde les questions dans le fichier JSON"""
    file_path = f"data/{theme}.json"
    os.makedirs('data', exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"[{theme}] 💾 Sauvegardé: {len(questions)} questions dans {file_path}")

def main():
    print("="*70)
    print("Génération de questions via API OpenAI GPT")
    print("="*70)
    
    # Vérification de la clé API
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ ERREUR: Variable d'environnement OPENAI_API_KEY non définie")
        print("\nExécute: export OPENAI_API_KEY=\"sk-...\"")
        return
    
    for theme, description in THEMES.items():
        # Charge les questions existantes
        existing = load_existing_questions(theme)
        existing_count = len(existing)
        
        print(f"\n{'='*70}")
        print(f"Thème: {theme.upper()}")
        print(f"Questions existantes: {existing_count}")
        print(f"{'='*70}")
        
        if existing_count >= 200:
            print(f"[{theme}] ✓ Déjà {existing_count} questions, skip")
            continue
        
        # Calcule combien de questions à générer
        to_generate = 200 - existing_count
        
        # Génère les nouvelles questions
        new_questions = generate_questions_with_gpt(theme, description, to_generate)
        
        if new_questions:
            # Combine avec les existantes
            all_questions = existing + new_questions
            
            # Sauvegarde
            save_questions(theme, all_questions[:200])
        else:
            print(f"[{theme}] ⚠️  Aucune question générée, conservation des existantes")
    
    print("\n" + "="*70)
    print("✅ TERMINÉ: Tous les fichiers ont été traités!")
    print("="*70)
    print("\nCoût estimé: ~$0.20-0.50 selon le modèle utilisé")

if __name__ == "__main__":
    main()
