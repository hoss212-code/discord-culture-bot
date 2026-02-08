import json
import random
import sqlite3
from config import QUESTIONS_JSON_PATH, QUESTIONS_DB_PATH

async def load_questions():
    """Load questions from JSON to SQLite cache"""
    try:
        with open(QUESTIONS_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conn = sqlite3.connect(QUESTIONS_DB_PATH)
        cursor = conn.cursor()
        
        # Create questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL,
                theme TEXT NOT NULL,
                difficulty INTEGER,
                answer_a TEXT,
                answer_b TEXT,
                answer_c TEXT,
                answer_d TEXT,
                correct_answer TEXT
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_theme ON questions(theme)')
        
        # Clear and insert questions
        cursor.execute('DELETE FROM questions')
        
        for q in data.get('questions', []):
            answers = q.get('answers', [])
            answer_a = answers[0]['text'] if len(answers) > 0 else ''
            answer_b = answers[1]['text'] if len(answers) > 1 else ''
            answer_c = answers[2]['text'] if len(answers) > 2 else ''
            answer_d = answers[3]['text'] if len(answers) > 3 else ''
            correct = [a['text'] for a in answers if a.get('correct')][0] if answers else ''
            
            cursor.execute('''
                INSERT INTO questions (question, theme, difficulty, answer_a, answer_b, answer_c, answer_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (q['question'], q.get('theme', 'general'), q.get('difficulty', 1), answer_a, answer_b, answer_c, answer_d, correct))
        
        conn.commit()
        conn.close()
        print(f'✅ Loaded {len(data.get("questions", []))} questions')
    except FileNotFoundError:
        print('⚠️ questions.json not found, creating empty database')

def get_random_question(theme=None):
    """Get random question, optionally filtered by theme"""
    conn = sqlite3.connect(QUESTIONS_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if theme:
        cursor.execute('SELECT * FROM questions WHERE theme = ? ORDER BY RANDOM() LIMIT 1', (theme,))
    else:
        cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
    
    question = cursor.fetchone()
    conn.close()
    
    return dict(question) if question else None

def get_questions_by_theme(theme):
    """Get all questions for a theme"""
    conn = sqlite3.connect(QUESTIONS_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM questions WHERE theme = ?', (theme,))
    questions = [dict(q) for q in cursor.fetchall()]
    conn.close()
    
    return questions
