import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

# Add your Twitch API credentials here
TWITCH_CLIENT_ID = 'your_client_id'
TWITCH_CLIENT_SECRET = 'your_client_secret'

import sqlite3
from config.settings import DATABASE

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          image_url TEXT NOT NULL,
                          info TEXT,
                          quality TEXT NOT NULL,
                          save_duration TEXT NOT NULL,
                          record_length INTEGER,
                          favorited INTEGER DEFAULT 0)''')
        conn.commit()


if __name__ == '__main__':
    init_db()
