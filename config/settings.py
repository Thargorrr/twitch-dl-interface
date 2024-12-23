import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')
ENV_PATH = os.path.join(BASE_DIR, '..', '.env')

def initialize():
    if not os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'w') as f:
            f.write('')  # Create an empty .env file

initialize()

# Load environment variables from .env file
load_dotenv(ENV_PATH)
print(f"SECRET_KEY from settings.py: {os.getenv('SECRET_KEY')}")

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

def get_database_path():
    # Import DATABASE here to avoid circular import
    from config.settings import DATABASE
    return DATABASE

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
                          record_length INTEGER
                          favorited INTEGER DEFAULT 0)''')
        conn.commit()

if __name__ == '__main__':
    init_db()
