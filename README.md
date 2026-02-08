# 🎮 Discord Culture Bot

Bot Discord pour jeux de culture générale en Python avec plusieurs modes de jeu compétitifs.

## 📝 Description

Ce bot Discord offre une expérience de quiz interactif avec plusieurs modes de jeu:
- **Battle Royale** : Tous contre tous avec élimination progressive
- **Duels** : Affrontements en 1v1, 2v2 ou 3v3 avec mécanique "l'épervier"
- **Questions Quotidiennes** : Questions automatiques à intervalles réguliers
- **Classement** : Système de points et statistiques détaillées

## ✨ Fonctionnalités

### Modes de jeu
- 💥 **Battle Royale** : Mode compétitif réservé aux admins avec limites configurables
- ⚔️ **Duels** : Création de salons temporaires pour des duels privés
  - Mode ouvert : `+duel 2v2`
  - Mode direct : `+duel 2v2 @joueur1 @joueur2 @joueur3`
- 📅 **Daily Quiz** : Questions envoyées automatiquement (intervalles de 12h ou 24h)
- 🏆 **Leaderboard** : Classement global et par serveur

### Système de points
- **2 points** pour une bonne réponse
- **x2 multiplicateur** si toute l'équipe répond correctement (= 4 points)
- Mécanique "l'épervier" : possibilité de sauver les coéquipiers éliminés

### Thèmes de questions
7 catégories disponibles:
- 🌍 Géographie
- 📜 Histoire
- 🎭 Culture générale
- 💻 Technologie
- 🔬 Science
- ⚽ Sport
- ⚽ Football

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Un bot Discord (créé sur le [Discord Developer Portal](https://discord.com/developers/applications))

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/hoss212-code/discord-culture-bot.git
cd discord-culture-bot
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer le bot**

Créer un fichier `.env` à la racine du projet:
```env
DISCORD_TOKEN=votre_token_ici
DISCORD_PREFIX=+
```

4. **Lancer le bot**
```bash
python main.py
```

## 📚 Commandes

### Configuration (Admin uniquement)
- `/setup` - Configuration initiale du serveur
- `/set_br_channel #salon` - Définir le salon Battle Royale
- `/set_daily_channel #salon` - Définir le salon des questions quotidiennes
- `/add_br_admin @membre` - Ajouter un admin Battle Royale

### Jeu
- `+duel 1v1 | 2v2 | 3v3` - Lancer un duel
- `+duel 2v2 @joueur1 @joueur2 @joueur3` - Duel avec mentions
- `/leaderboard [global|server]` - Afficher le classement
- `/stats [@membre]` - Voir les statistiques

## 📁 Structure du projet

```
discord-culture-bot/
├── cogs/                  # Modules du bot
│   ├── battle_royale.py
│   ├── duel.py
│   ├── daily_quiz.py
│   ├── leaderboard.py
│   └── setup.py
├── data/                  # Données
│   ├── *.json             # Questions par thème
│   └── bot_data.db        # Base SQLite (générée auto)
├── utils/                 # Utilitaires
│   ├── database.py
│   └── questions.py
├── main.py                # Point d'entrée
├── config.py              # Configuration
├── requirements.txt       # Dépendances
└── README_QUESTIONS.md    # Guide pour ajouter des questions
```

## 💾 Base de données

Le bot utilise **SQLite** pour stocker:
- Statistiques des joueurs (points, victoires, défaites)
- Historique des parties
- Classements par serveur

La base est créée automatiquement au premier lancement dans `data/bot_data.db`.

## ➕ Ajouter des questions

Consulte le fichier [README_QUESTIONS.md](README_QUESTIONS.md) pour savoir comment compléter les fichiers JSON avec 120 questions par thème.

**Format d'une question:**
```json
{
  "question": "Quelle est la capitale de la France?",
  "options": ["Paris", "Lyon", "Marseille", "Toulouse"],
  "correct": 0,
  "theme": "geography",
  "difficulty": "facile"
}
```

## 🔧 Technologies

- **Python 3.8+**
- **discord.py** - Librairie Discord
- **SQLite** - Base de données
- **asyncio** - Programmation asynchrone

## 📝 Licence

Ce projet est sous licence MIT.

## 👥 Contribution

Les contributions sont les bienvenues! N'hésite pas à ouvrir une issue ou une pull request.

## 🚀 Auteur

Créé avec ❤️ par [hoss212-code](https://github.com/hoss212-code)
