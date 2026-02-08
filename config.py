import os
from dotenv import load_dotenv

load_dotenv()

# Discord
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_PREFIX = '+'

# Database
DB_PATH = 'data/bot_data.db'
QUESTIONS_DB_PATH = 'data/questions.db'
QUESTIONS_JSON_PATH = 'data/questions.json'

# Game Settings
QUESTION_TIME_LIMIT = 15  # seconds
BATTLE_ROYALE_QUESTIONS = 10
DUEL_QUESTIONS = 10
DAILY_QUIZ_TIME = "08:00"  # HH:MM format
DAILY_QUIZ_INTERVAL = 24  # hours

# Points System
BASE_POINTS = 2
BONUS_MULTIPLIER = 2  # x2 when all team correct
RESCUE_POINTS = 1

# Themes
THEMES = {
    'geography': '🌍 Géographie',
    'history': '📚 Histoire',
    'culture_generale': '🎨 Culture Générale',
    'technologie': '💻 Technologie',
    'science': '🔬 Science',
    'sports': '🏀 Sports',
    'football': '⚽ Football',
}

# Colors
COLOR_PRIMARY = 0x00B4D8
COLOR_SUCCESS = 0x06D6A0
COLOR_ERROR = 0xEF476F
COLOR_WARNING = 0xFFD60A
