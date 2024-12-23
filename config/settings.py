from dotenv import load_dotenv
import sqlite3
from backend.db.operations import initialize, ENV_PATH, DATABASE


initialize()

# Load environment variables from .env file
load_dotenv(ENV_PATH)

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

if __name__ == '__main__':
    init_db()
