import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:@localhost/smart_recovery')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465  # Change to SSL port
    MAIL_USE_TLS = False  # Disable TLS
    MAIL_USE_SSL = True   # Enable SSL
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'frontend/uploads'

    # Matching Configuration
    SQLALCHEMY_ECHO = True  # This will log all database operations
    MATCH_THRESHOLD = 0.5  # 50% description accuracy threshold
    TIME_WEIGHT = 0.3      # 30% time accuracy weight
    LOCATION_WEIGHT = 0.2  # 20% location accuracy weight 