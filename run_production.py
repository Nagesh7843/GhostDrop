"""GhostDrop - Production Server with Waitress"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create application
config_name = os.environ.get('FLASK_ENV', 'production')
app = create_app(config_name)

if __name__ == '__main__':
    from waitress import serve
    
    host = app.config['HOST']
    port = app.config['PORT']
    
    print("\n" + "="*60)
    print("🚀 GhostDrop Production Server")
    print("="*60)
    print(f"Environment: {config_name}")
    print(f"Running on: http://{host}:{port}")
    print(f"Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Run with Waitress (production-ready WSGI server)
    serve(app, host=host, port=port, threads=4)
