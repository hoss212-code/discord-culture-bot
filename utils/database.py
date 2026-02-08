import sqlite3
import os
from config import DB_PATH, QUESTIONS_DB_PATH

async def init_database():
    """Initialize SQLite databases for the bot"""
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Initialize bot_data.db
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            total_points INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            victories INTEGER DEFAULT 0,
            defeats INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Game history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_type TEXT NOT NULL,
            points INTEGER,
            result TEXT,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Streaks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streaks (
            user_id INTEGER PRIMARY KEY,
            current_streak INTEGER DEFAULT 0,
            best_streak INTEGER DEFAULT 0,
            last_correct_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print('✅ Database initialized')

def get_user_stats(user_id: int) -> dict:
    """Get user statistics from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return dict(user)
    return None

def add_points(user_id: int, points: int, game_type: str):
    """Add points to user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, f'User_{user_id}'))
    cursor.execute('UPDATE users SET total_points = total_points + ? WHERE user_id = ?', (points, user_id))
    cursor.execute('INSERT INTO game_history (user_id, game_type, points) VALUES (?, ?, ?)', (user_id, game_type, points))
    
    conn.commit()
    conn.close()
