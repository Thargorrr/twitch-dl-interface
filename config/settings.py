import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import sqlite3
from config.settings import DATABASE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')
ENV_PATH = os.path.join(BASE_DIR, '..', '.env')

# Load environment variables from .env file
load_dotenv(ENV_PATH)

# Generate SECRET_KEY if it doesn't exist
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = Fernet.generate_key().decode()
    with open(ENV_PATH, 'a') as f:
        f.write(f'\nSECRET_KEY={SECRET_KEY}')

cipher = Fernet(SECRET_KEY.encode())

def encrypt_data(data):
    """Encrypt the data."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypt the data."""
    return cipher.decrypt(data.encode()).decode()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          url TEXT NOT NULL,
                          quality TEXT NOT NULL,
                          save_duration TEXT NOT NULL,
                          record_length INTEGER
                          )''')

        cursor.execute('''INSERT OR IGNORE INTO settings (id) VALUES (1)''')
        conn.commit()

if __name__ == '__main__':
    init_db()
