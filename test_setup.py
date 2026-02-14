"""
Test script to verify GhostDrop installation and basic functionality
"""
import os
import sys

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    try:
        import flask
        import pymongo
        import bcrypt
        import apscheduler
        import werkzeug
        from dotenv import load_dotenv
        print("   ✓ All imports successful")
        return True
    except ImportError as e:
        print(f"   ✗ Import error: {e}")
        return False

def test_directory_structure():
    """Test project directory structure"""
    print("\n🧪 Testing directory structure...")
    required_dirs = [
        'app',
        'app/templates',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/utils',
        'uploads'
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"   ✓ {dir_path}")
        else:
            print(f"   ✗ {dir_path} NOT FOUND")
            all_ok = False
    
    return all_ok

def test_required_files():
    """Test required files exist"""
    print("\n🧪 Testing required files...")
    required_files = [
        'run.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'app/__init__.py',
        'app/models.py',
        'app/routes.py',
        'app/utils/security.py',
        'app/utils/file_handler.py',
        'app/utils/cleanup.py',
        'app/templates/base.html',
        'app/templates/index.html',
        'app/templates/upload.html',
        'app/templates/download.html',
        'app/templates/error.html',
        'app/static/css/style.css',
        'app/static/js/main.js'
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} NOT FOUND")
            all_ok = False
    
    return all_ok

def test_env_file():
    """Check if .env exists"""
    print("\n🧪 Testing environment configuration...")
    if os.path.exists('.env'):
        print("   ✓ .env file exists")
        return True
    else:
        print("   ⚠ .env file not found")
        print("   → Copy .env.example to .env and configure")
        return False

def test_config():
    """Test config loading"""
    print("\n🧪 Testing configuration...")
    try:
        from config import config
        default_config = config['default']
        print(f"   ✓ Config loaded")
        print(f"   - Upload folder: {default_config.UPLOAD_FOLDER}")
        print(f"   - Token length: {default_config.TOKEN_LENGTH}")
        print(f"   - Max file size: {default_config.MAX_CONTENT_LENGTH / (1024*1024):.0f}MB")
        return True
    except Exception as e:
        print(f"   ✗ Config error: {e}")
        return False

def test_app_creation():
    """Test Flask app creation"""
    print("\n🧪 Testing Flask app creation...")
    try:
        from app import create_app
        app = create_app('development')
        print("   ✓ Flask app created successfully")
        print(f"   - App name: {app.name}")
        print(f"   - Debug mode: {app.config['DEBUG']}")
        return True
    except Exception as e:
        print(f"   ✗ App creation error: {e}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\n🧪 Testing MongoDB connection...")
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("   ✓ MongoDB is running and accessible")
        client.close()
        return True
    except Exception as e:
        print(f"   ⚠ MongoDB connection failed: {e}")
        print("   → Make sure MongoDB is installed and running")
        print("   → Start with: net start MongoDB (Windows)")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🚀 GhostDrop Installation Verification")
    print("="*60)
    
    tests = [
        test_imports,
        test_directory_structure,
        test_required_files,
        test_env_file,
        test_config,
        test_app_creation,
        test_mongodb_connection
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"   ✗ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed ({passed}/{total})")
        print("\n🎉 GhostDrop is ready to run!")
        print("\nStart the application with:")
        print("   python run.py")
        return 0
    else:
        print(f"⚠️ {passed}/{total} tests passed")
        print("\n🔧 Please fix the above issues before running")
        return 1

if __name__ == '__main__':
    sys.exit(main())
