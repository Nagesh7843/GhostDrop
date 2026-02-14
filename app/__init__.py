"""Flask application factory"""
import os
from flask import Flask
from app.utils import RateLimiter
from app.models import DatabaseManager
from app.utils.cleanup import CleanupManager
from config import config

def create_app(config_name='default'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    db_manager = DatabaseManager(
        app.config['MONGODB_URI'],
        app.config['MONGODB_DB_NAME']
    )
    
    # Test database connection
    if not db_manager.ping():
        print("⚠ Warning: Could not connect to MongoDB. Make sure MongoDB is running.")
    else:
        print("✓ Connected to MongoDB")
    
    # Initialize rate limiter
    rate_limiter = RateLimiter()
    
    # Store in app config
    app.config['DB_MANAGER'] = db_manager
    app.config['RATE_LIMITER'] = rate_limiter
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Initialize cleanup manager
    cleanup_manager = CleanupManager(app, db_manager.db)
    cleanup_manager.start()
    app.config['CLEANUP_MANAGER'] = cleanup_manager
    
    print(f"✓ GhostDrop initialized")
    print(f"  - Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"  - Max file size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.0f}MB")
    print(f"  - Rate limit: {app.config['MAX_REQUESTS_PER_MINUTE']} requests/minute")
    
    return app
