import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    DATABASE = os.getenv("DATABASE", "database.db")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    WTF_CSRF_ENABLED = True