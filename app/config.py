import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set")
    
    DATABASE = os.getenv("DATABASE", "database.db")

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    WTF_CSRF_ENABLED = True

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = False