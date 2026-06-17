import os

class Config:
    # Secret key for session management
    SECRET_KEY = 'your_secret_key_here'

    # Database configuration (SQLite)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

    # Disable modification tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    SESSION_TYPE = 'filesystem'

    # Quiz default duration (in minutes)
    DEFAULT_QUIZ_DURATION = 60