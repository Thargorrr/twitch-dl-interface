import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')
ENV_PATH = os.path.join(BASE_DIR, '..', '.env')

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          channel_id TEXT NOT NULL,
                          channel_name TEXT NOT NULL,
                          image_url TEXT NOT NULL,
                          info TEXT,
                          quality TEXT NOT NULL,
                          save_duration TEXT NOT NULL,
                          record_length INTEGER
                          )''')
        conn.commit()

def get_channel(channel_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM channels WHERE id = ?', (channel_id,))
        return cursor.fetchone()

def update_channel_config(channel_id, form):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE channels SET 
                          recording = ?, quality = ?, save_duration = ?, record_length = ?
                          WHERE id = ?''',
                       (form['recording'], form['quality'], form['save_duration'], form['record_length'], channel_id))
        conn.commit()

def search_channels(query):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, name, url FROM channels WHERE name LIKE ? LIMIT 10',
            (f'%{query}%',),
        )
        return cursor.fetchall()
    
# Ensure the database and tables are created
init_db()