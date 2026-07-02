import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'bektour-secret-2026-change-this')
    # PostgreSQL on Railway, SQLite locally
    DB = os.environ.get('DATABASE_URL', 'sqlite:///villasite.db')
    # Fix legacy postgres:// → postgresql://
    if DB and DB.startswith('postgres://'):
        DB = DB.replace('postgres://', 'postgresql://', 1)
    # Use psycopg3 binary driver (postgresql+psycopg://)
    if DB and DB.startswith('postgresql://'):
        DB = DB.replace('postgresql://', 'postgresql+psycopg://', 1)
    SQLALCHEMY_DATABASE_URI = DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 10,
    }
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
