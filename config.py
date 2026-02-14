import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    
    # MongoDB
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME', 'ghostdrop')
    
    # File Storage
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
        'xls', 'xlsx', 'zip', 'rar', '7z', 'mp4', 'mp3', 'avi', 
        'mov', 'ppt', 'pptx', 'csv', 'json', 'xml'
    }
    
    # Security
    TOKEN_LENGTH = 6
    MAX_REQUESTS_PER_MINUTE = 10  # Rate limiting
    PASSWORD_MIN_LENGTH = 4
    
    # Expiry Options
    EXPIRY_OPTIONS = {
        '1hour': timedelta(hours=1),
        '6hours': timedelta(hours=6),
        '1day': timedelta(days=1),
        '3days': timedelta(days=3),
        '7days': timedelta(days=7)
    }
    
    # Cleanup
    CLEANUP_INTERVAL_MINUTES = 5  # Run cleanup every 5 minutes
    
    # Deployment
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Force HTTPS in production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
