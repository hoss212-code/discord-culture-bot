#!/usr/bin/env python3
"""
Script pour convertir le fichier texte de questions généré par ChatGPT en JSON valide

Utilisation:
    python3 convert_to_json.py input.txt output.json
    
Exemple:
    python3 convert_to_json.py paste.txt data/culture_generale.json
"""

import json
import re
import sys

def parse_text_to_json(input_file):
    """Parse le fichier texte et extrait les questions en JSON"""
    questions = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour matcher chaque question
    # Format: question XXX Variante N, options A, B, C, D , correct N, theme XXX, difficulty XXX
    pattern = r'question\s+([^?]+\?)[^,]*,\s*options\s+([^,]+),\s+([^,]+),\s+([^,]+),\s+([^,]+)\s*,\s*correct\s+(\d+),\s*theme\s+(\w+),\s*difficulty\s+(\w+)'
    
    matches = re.findall(pattern, content)
    
    for match in matches:
        question_text = match[0].strip()
        option1 = match[1].strip()
        option2 = match[2].strip()
        option3 = match[3].strip()
        option4 = match[4].strip()
        correct_idx = int(match[5])
        theme = match[6]
        difficulty = match[7]
        
        question_obj = {
            "question": question_text,
            "options": [option1, option2, option3, option4],
            "correct": correct_idx,
            "theme": theme,
            "difficulty": difficulty
        }
        
        questions.append(question_obj)
    
    return questions

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 convert_to_json.py <input.txt> <output.json>")
        print("Exemple: python3 convert_to_json.py paste.txt data/culture_generale.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"Lecture du fichier: {input_file}")
    questions = parse_text_to_json(input_file)
    
    print(f"Questions extraites: {len(questions)}")
    
    # Sauvegarde en JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Conversion réussie: {output_file}")
    print(f"Total: {len(questions)} questions")

if __name__ == "__main__":
    main()
