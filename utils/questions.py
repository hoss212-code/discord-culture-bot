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


def get_unique_question(mode='daily', theme=None, guild_id=None):
    """Get a question that hasn't been used recently for this mode
    
    Args:
        mode: 'daily', 'battle_royale', 'multiplayer', 'duel'
        theme: Optional theme filter
        guild_id: Server ID for tracking per-server usage
    
    Returns:
        dict: Question data or None
    """
    conn = sqlite3.connect(QUESTIONS_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create question_usage table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question_usage (
            question_id INTEGER,
            mode TEXT,
            guild_id TEXT,
            used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (question_id, mode, guild_id)
        )
    ''')
    
    # Get total number of questions for the theme
    if theme:
        cursor.execute('SELECT COUNT(*) as total FROM questions WHERE theme = ?', (theme,))
    else:
        cursor.execute('SELECT COUNT(*) as total FROM questions')
    total_questions = cursor.fetchone()['total']
    
    # Get number of used questions for this mode/guild
    if theme:
        cursor.execute('''
            SELECT COUNT(DISTINCT q.id) as used 
            FROM questions q 
            INNER JOIN question_usage u ON q.id = u.question_id 
            WHERE u.mode = ? AND u.guild_id = ? AND q.theme = ?
        ''', (mode, str(guild_id or 'global'), theme))
    else:
        cursor.execute('''
            SELECT COUNT(DISTINCT question_id) as used 
            FROM question_usage 
            WHERE mode = ? AND guild_id = ?
        ''', (mode, str(guild_id or 'global')))
    used_count = cursor.fetchone()['used']
    
    # If we've used all questions, reset the pool
    if used_count >= total_questions:
        cursor.execute('''
            DELETE FROM question_usage 
            WHERE mode = ? AND guild_id = ?
        ''', (mode, str(guild_id or 'global')))
        conn.commit()
        print(f'🔄 Reset question pool for {mode} (used all {total_questions} questions)')
    
    # Get a random question that hasn't been used yet
    if theme:
        cursor.execute('''
            SELECT q.* FROM questions q
            LEFT JOIN question_usage u 
                ON q.id = u.question_id 
                AND u.mode = ? 
                AND u.guild_id = ?
            WHERE u.question_id IS NULL 
                AND q.theme = ?
            ORDER BY RANDOM() 
            LIMIT 1
        ''', (mode, str(guild_id or 'global'), theme))
    else:
        cursor.execute('''
            SELECT q.* FROM questions q
            LEFT JOIN question_usage u 
                ON q.id = u.question_id 
                AND u.mode = ? 
                AND u.guild_id = ?
            WHERE u.question_id IS NULL
            ORDER BY RANDOM() 
            LIMIT 1
        ''', (mode, str(guild_id or 'global')))
    
    question = cursor.fetchone()
    
    if question:
        # Mark question as used
        question_dict = dict(question)
        cursor.execute('''
            INSERT OR REPLACE INTO question_usage (question_id, mode, guild_id)
            VALUES (?, ?, ?)
        ''', (question_dict['id'], mode, str(guild_id or 'global')))
        conn.commit()
    
    conn.close()
    return dict(question) if question else None


def reset_question_pool(mode=None, guild_id=None):
    """Manually reset the question pool for a specific mode/guild
    
    Args:
        mode: Specific mode to reset, or None for all modes
        guild_id: Specific guild, or None for global
    """
    conn = sqlite3.connect(QUESTIONS_DB_PATH)
    cursor = conn.cursor()
    
    if mode and guild_id:
        cursor.execute('DELETE FROM question_usage WHERE mode = ? AND guild_id = ?', 
                      (mode, str(guild_id)))
        print(f'✅ Reset {mode} question pool for guild {guild_id}')
    elif mode:
        cursor.execute('DELETE FROM question_usage WHERE mode = ?', (mode,))
        print(f'✅ Reset {mode} question pool for all guilds')
    elif guild_id:
        cursor.execute('DELETE FROM question_usage WHERE guild_id = ?', (str(guild_id),))
        print(f'✅ Reset all question pools for guild {guild_id}')
    else:
        cursor.execute('DELETE FROM question_usage')
        print('✅ Reset all question pools')
    
    conn.commit()
    conn.close()
    
    return questions
