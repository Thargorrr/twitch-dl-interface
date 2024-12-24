from dotenv import load_dotenv
from backend.db.operations import ENV_PATH
from backend.initialization import initialize

initialize()

# Load environment variables from .env file
load_dotenv(ENV_PATH)
