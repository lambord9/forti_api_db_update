from dotenv import load_dotenv
import os

load_dotenv()
path = os.path.dirname(os.path.realpath(__name__))

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/devices"

UPDATES_PATH = os.path.join(path, 'updates')