import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseCreds:
    USER = os.getenv('DB_MOVIES_USER')
    PASSWORD = os.getenv('DB_MOVIES_PASSWORD')
    HOST = os.getenv('DB_MOVIES_HOST')
    PORT = os.getenv('DB_MOVIES_PORT')
    NAME = os.getenv('DB_MOVIES_NAME')