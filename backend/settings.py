import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'trivia')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password123!')
