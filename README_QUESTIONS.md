README_QUESTIONS.md# Guide pour compléter les questions du bot

## 📊 État actuel

Actuellement, chaque fichier JSON dans le dossier `data/` contient entre 7 et 10 questions.
**Objectif: 120 questions par thème** (840 questions au total)

### Fichiers à compléter:
- `culture_generale.json` - 10/120 questions ❌
- `football.json` - 7/120 questions ❌
- `geography.json` - 10/120 questions ❌
- `history.json` - 10/120 questions ❌
- `science.json` - 3/120 questions ❌
- `sport.json` - 3/120 questions ❌
- `technology.json` - 5/120 questions ❌

## 📝 Format des questions

Chaque question doit suivre ce format JSON exact:

```json
{
  "question": "Votre question ici?",
  "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"],
  "correct": 0,
  "theme": "nom_du_theme",
  "difficulty": "facile"
}
```

### Explications:
- `question`: La question en français
- `options`: 4 réponses possibles
- `correct`: Index de la bonne réponse (0 pour la 1ère, 1 pour la 2ème, etc.)
- `theme`: Nom du thème (doit correspondre au nom du fichier)
- `difficulty`: "facile", "moyen", ou "difficile"

## 🎯 Répartition recommandée par difficulté

Sur 120 questions par thème:
- **50 faciles** (42%)
- **50 moyennes** (42%)
- **20 difficiles** (16%)

## 💡 Exemples par thème

### Geography (geography.json)
```json
{
  "question": "Quelle est la capitale de l'Australie?",
  "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
  "correct": 2,
  "theme": "geography",
  "difficulty": "moyen"
}
```

### History (history.json)
```json
{
  "question": "En quelle année a débuté la Première Guerre mondiale?",
  "options": ["1912", "1914", "1916", "1918"],
  "correct": 1,
  "theme": "history",
  "difficulty": "facile"
}
```

### Science (science.json)
```json
{
  "question": "Quel est le symbole chimique du sodium?",
  "options": ["So", "Na", "Sd", "S"],
  "correct": 1,
  "theme": "science",
  "difficulty": "moyen"
}
```

### Football (football.json)
```json
{
  "question": "Quel club a remporté la Ligue des Champions 2023?",
  "options": ["Real Madrid", "Manchester City", "Bayern Munich", "PSG"],
  "correct": 1,
  "theme": "football",
  "difficulty": "facile"
}
```

## 🚀 Comment ajouter les questions

### Méthode 1: Directement sur GitHub
1. Ouvrir le fichier JSON dans `data/`
2. Cliquer sur le crayon ✏️ (Edit)
3. Ajouter les questions en respectant le format
4. Commit les changements

### Méthode 2: En local (RECOMMANDÉ)
1. Cloner le repo: `git clone https://github.com/hoss212-code/discord-culture-bot.git`
2. Ouvrir les fichiers JSON dans un éditeur
3. Ajouter les questions
4. Commit et push: 
   ```bash
   git add data/
   git commit -m "feat: Ajout questions [nom_theme]"
   git push
   ```

### Méthode 3: Utiliser ChatGPT/IA
Tu peux demander à ChatGPT de générer des questions:

**Prompt exemple:**
> "Génère 30 questions de culture générale de niveau facile au format JSON suivant: {"question": "...", "options": [...], "correct": X, "theme": "culture_generale", "difficulty": "facile"}"

## ⚠️ Points d'attention

- ✅ **Toujours** 4 options de réponse
- ✅ Questions **en français**
- ✅ Une seule bonne réponse par question
- ✅ Difficultés variées
- ✅ Questions précises et non ambiguës
- ❌ Pas de caractères spéciaux non échappés
- ❌ Pas de virgule après la dernière question du tableau

## 📚 Ressources

- OpenTriviaDB (adapter en français)
- Quizz en ligne français
- Livres de culture générale
- Sites éducatifs

## 🎮 Test du bot

Après avoir ajouté des questions:
1. Lancer le bot: `python main.py`
2. Utiliser les commandes pour tester
3. Vérifier que les questions s'affichent correctement

Bon courage ! 🚀
