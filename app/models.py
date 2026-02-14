"""Database models and operations for GhostDrop"""
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

class FileModel:
    """Handles file database operations"""
    
    def __init__(self, db):
        self.collection = db.files
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create necessary indexes for performance and uniqueness"""
        try:
            # Unique index on code
            self.collection.create_index('code', unique=True)
            # Index on expires_at for cleanup queries
            self.collection.create_index('expires_at')
            # Index on created_at for analytics
            self.collection.create_index('created_at')
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")
    
    def create_file_entry(self, code, filename, file_path, file_size, 
                         expiry_type, expiry_value, max_downloads=None, 
                         password_hash=None, original_filename=None):
        """
        Create a new file entry in the database
        
        Args:
            code: Unique access code
            filename: Stored filename
            file_path: Path to file (relative to upload folder)
            file_size: Size in bytes
            expiry_type: 'time' or 'download'
            expiry_value: timedelta for time-based, int for download-based
            max_downloads: Max downloads allowed (for download-based expiry)
            password_hash: Hashed password (optional)
            original_filename: Original uploaded filename
        """
        now = datetime.utcnow()
        
        # Calculate expiration
        if expiry_type == 'time':
            expires_at = now + expiry_value
        elif expiry_type == 'download':
            # For download-based, set far future expiry as backup
            expires_at = now + timedelta(days=30)
        elif expiry_type == 'onetime':
            # One-time download
            expires_at = now + timedelta(days=7)  # 7 days max
            max_downloads = 1
        else:
            expires_at = now + timedelta(days=7)
        
        file_doc = {
            'code': code,
            'filename': filename,
            'file_path': file_path,
            'original_filename': original_filename or filename,
            'file_size': file_size,
            'file_size_human': self._format_size(file_size),
            'expiry_type': expiry_type,
            'created_at': now,
            'expires_at': expires_at,
            'max_downloads': max_downloads,
            'current_downloads': 0,
            'password_protected': password_hash is not None,
            'password_hash': password_hash,
            'last_accessed': None,
            'ip_address': None,  # Can be stored for analytics
            'deleted': False
        }
        
        try:
            result = self.collection.insert_one(file_doc)
            return True, result.inserted_id
        except DuplicateKeyError:
            return False, "Code already exists"
        except Exception as e:
            return False, str(e)
    
    def get_file_by_code(self, code):
        """Retrieve file by access code"""
        return self.collection.find_one({'code': code, 'deleted': False})
    
    def increment_download_count(self, code):
        """Increment download counter and check if file should be deleted"""
        result = self.collection.find_one_and_update(
            {'code': code},
            {
                '$inc': {'current_downloads': 1},
                '$set': {'last_accessed': datetime.utcnow()}
            },
            return_document=True
        )
        
        if not result:
            return None, "File not found"
        
        # Check if download limit reached
        if result.get('max_downloads'):
            if result['current_downloads'] >= result['max_downloads']:
                return result, "DELETE"  # Signal to delete
        
        return result, "OK"
    
    def delete_file(self, code):
        """Mark file as deleted"""
        result = self.collection.update_one(
            {'code': code},
            {'$set': {'deleted': True, 'deleted_at': datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    def hard_delete_file(self, code):
        """Permanently delete file from database"""
        result = self.collection.delete_one({'code': code})
        return result.deleted_count > 0
    
    def get_expired_files(self):
        """Get all expired files"""
        return self.collection.find({
            'expires_at': {'$lt': datetime.utcnow()},
            'deleted': False
        })
    
    def get_stats(self):
        """Get database statistics"""
        total = self.collection.count_documents({})
        active = self.collection.count_documents({'deleted': False})
        expired = self.collection.count_documents({
            'expires_at': {'$lt': datetime.utcnow()},
            'deleted': False
        })
        
        return {
            'total': total,
            'active': active,
            'expired': expired
        }
    
    @staticmethod
    def _format_size(size_bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"


class DatabaseManager:
    """Manages database connection and models"""
    
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.files = FileModel(self.db)
    
    def ping(self):
        """Check if database is reachable"""
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        self.client.close()
