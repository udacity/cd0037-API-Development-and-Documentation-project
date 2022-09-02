from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_TEST_NAME=os.getenv('DB_TEST_NAME')