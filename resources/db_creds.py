import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseCreds:
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')