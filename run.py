"""GhostDrop - Main application entry point"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Determine configuration
config_name = os.environ.get('FLASK_ENV', 'development')

# Create application
app = create_app(config_name)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting GhostDrop")
    print("="*60)
    print(f"Environment: {config_name}")
    print(f"Debug Mode: {app.config['DEBUG']}")
    print(f"Host: {app.config['HOST']}")
    print(f"Port: {app.config['PORT']}")
    print("="*60 + "\n")
    
    # Run the application
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
