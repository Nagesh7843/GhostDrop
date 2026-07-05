#!/usr/bin/env python3
"""Test MongoDB Atlas connection"""

import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ghostdrop")

print("🔍 Testing MongoDB Connection...\n")
print(f"URI: {MONGODB_URI}\n")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Try to connect
    client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas successfully!\n")
    
    # Get database
    db = client[MONGODB_DB_NAME]
    print(f"✅ Database '{MONGODB_DB_NAME}' accessible\n")
    
    # List collections
    collections = db.list_collection_names()
    print(f"📊 Collections: {collections if collections else 'None (will be created on first use)'}\n")
    
    print("✨ MongoDB is working correctly!")
    sys.exit(0)
    
except ServerSelectionTimeoutError as e:
    print(f"❌ Connection timeout!\n")
    print(f"Error: {e}\n")
    print("Solutions:")
    print("1. Check MongoDB Atlas IP whitelist includes 0.0.0.0/0")
    print("2. Verify username/password are correct")
    print("3. Check if cluster is running (not paused)")
    print("4. Try disabling VPN/firewall temporarily")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error: {e}\n")
    print("Type:", type(e).__name__)
    sys.exit(1)
