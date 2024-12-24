import os
from backend.db.operations import ENV_PATH
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv(ENV_PATH, override=True)

def initialize():
    if not os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'w') as f:
            f.write('')  # Create an empty .env file

def encrypt_data(data):
    """Encrypt the data."""
    # Generate SECRET_KEY if it doesn't exist
    load_dotenv(ENV_PATH, override=True)
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        SECRET_KEY = Fernet.generate_key().decode()
        with open(ENV_PATH, 'a') as f:
            f.write(f'\nSECRET_KEY={SECRET_KEY}')
    cipher = Fernet(SECRET_KEY.encode())
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypt the data."""
    # Generate SECRET_KEY if it doesn't exist
    load_dotenv(ENV_PATH, override=True)
    SECRET_KEY = os.getenv('SECRET_KEY')
    cipher = Fernet(SECRET_KEY.encode())
    return cipher.decrypt(data.encode()).decode()