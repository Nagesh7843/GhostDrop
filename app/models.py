"""Database models and operations for GhostDrop using SQLite3"""
import os
import sqlite3
from datetime import datetime, timedelta

class FileModel:
    """Handles file database operations using SQLite"""
    
    def __init__(self, manager):
        self.manager = manager
    
    @staticmethod
    def _format_size(size_bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    @staticmethod
    def _row_to_dict(row):
        """Convert a SQLite Row object to a dictionary matching standard schema"""
        if not row:
            return None
        
        row_keys = row.keys()
        
        def parse_date(date_str):
            if not date_str:
                return None
            try:
                return datetime.fromisoformat(date_str)
            except ValueError:
                return None
        
        return {
            'code': row['code'],
            'filename': row['filename'],
            'file_path': row['file_path'],
            'original_filename': row['original_filename'],
            'file_size': row['file_size'],
            'file_size_human': row['file_size_human'],
            'expiry_type': row['expiry_type'],
            'created_at': parse_date(row['created_at']),
            'expires_at': parse_date(row['expires_at']),
            'max_downloads': row['max_downloads'],
            'current_downloads': row['current_downloads'],
            'password_protected': bool(row['password_protected']),
            'password_hash': row['password_hash'],
            'last_accessed': parse_date(row['last_accessed']),
            'ip_address': row['ip_address'],
            'deleted': bool(row['deleted']),
            'deleted_at': parse_date(row['deleted_at']) if 'deleted_at' in row_keys else None
        }
    
    def create_file_entry(self, code, filename, file_path, file_size, 
                          expiry_type, expiry_value, max_downloads=None, 
                          password_hash=None, original_filename=None):
        """Create a new file entry in the database"""
        now = datetime.utcnow()
        
        # Calculate expiration
        if expiry_type == 'time':
            expires_at = now + expiry_value
        elif expiry_type == 'download':
            expires_at = now + timedelta(days=30)
        elif expiry_type == 'onetime':
            expires_at = now + timedelta(days=7)
            max_downloads = 1
        else:
            expires_at = now + timedelta(days=7)
            
        try:
            with self.manager.get_connection() as conn:
                conn.execute('''
                    INSERT INTO files (
                        code, filename, file_path, original_filename, file_size, 
                        file_size_human, expiry_type, created_at, expires_at, 
                        max_downloads, current_downloads, password_protected, password_hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                ''', (
                    code, filename, file_path, original_filename or filename, file_size,
                    self._format_size(file_size), expiry_type, now.isoformat(), expires_at.isoformat(),
                    max_downloads, 1 if password_hash else 0, password_hash
                ))
                conn.commit()
            return True, code
        except sqlite3.IntegrityError:
            return False, "Code already exists"
        except Exception as e:
            return False, str(e)
            
    def get_file_by_code(self, code):
        """Retrieve file by access code"""
        try:
            with self.manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM files WHERE code = ? AND deleted = 0', (code,))
                row = cursor.fetchone()
                return self._row_to_dict(row)
        except Exception:
            return None
            
    def increment_download_count(self, code):
        """Increment download counter and check if file should be deleted"""
        try:
            with self.manager.get_connection() as conn:
                conn.execute('''
                    UPDATE files 
                    SET current_downloads = current_downloads + 1, last_accessed = ? 
                    WHERE code = ?
                ''', (datetime.utcnow().isoformat(), code))
                conn.commit()
                
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM files WHERE code = ?', (code,))
                row = cursor.fetchone()
                
                if not row:
                    return None, "File not found"
                
                result = self._row_to_dict(row)
                
                # Check if download limit reached
                if result.get('max_downloads'):
                    if result['current_downloads'] >= result['max_downloads']:
                        return result, "DELETE"
                        
                return result, "OK"
        except Exception as e:
            return None, str(e)
            
    def delete_file(self, code):
        """Mark file as deleted (soft delete)"""
        try:
            with self.manager.get_connection() as conn:
                conn.execute('''
                    UPDATE files 
                    SET deleted = 1, deleted_at = ? 
                    WHERE code = ?
                ''', (datetime.utcnow().isoformat(), code))
                conn.commit()
            return True
        except Exception:
            return False
            
    def hard_delete_file(self, code):
        """Permanently delete file from database"""
        try:
            with self.manager.get_connection() as conn:
                conn.execute('DELETE FROM files WHERE code = ?', (code,))
                conn.commit()
            return True
        except Exception:
            return False
            
    def get_expired_files(self):
        """Get all expired files"""
        try:
            now_str = datetime.utcnow().isoformat()
            with self.manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM files WHERE expires_at < ? AND deleted = 0', (now_str,))
                rows = cursor.fetchall()
                return [self._row_to_dict(row) for row in rows]
        except Exception:
            return []
            
    def get_stats(self):
        """Get database statistics"""
        try:
            now_str = datetime.utcnow().isoformat()
            with self.manager.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT COUNT(*) FROM files')
                total = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM files WHERE deleted = 0')
                active = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM files WHERE expires_at < ? AND deleted = 0', (now_str,))
                expired = cursor.fetchone()[0]
                
                return {
                    'total': total,
                    'active': active,
                    'expired': expired
                }
        except Exception:
            return {'total': 0, 'active': 0, 'expired': 0}


class DatabaseManager:
    """Manages SQLite database connections and schemas"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.files = FileModel(self)
        self._init_db()
        
    def get_connection(self):
        """Open a new database connection (thread-safe for Flask threads)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def _init_db(self):
        """Initialize database schema tables and indexes"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    code TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_size_human TEXT NOT NULL,
                    expiry_type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    max_downloads INTEGER,
                    current_downloads INTEGER DEFAULT 0,
                    password_protected INTEGER DEFAULT 0,
                    password_hash BLOB,
                    last_accessed TEXT,
                    ip_address TEXT,
                    deleted INTEGER DEFAULT 0,
                    deleted_at TEXT
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_files_expires_at ON files (expires_at)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_files_created_at ON files (created_at)')
            conn.commit()
            
    def ping(self):
        """Check if database is reachable"""
        try:
            with self.get_connection() as conn:
                conn.execute('SELECT 1')
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
            
    def close(self):
        """No-op for connection-per-query strategy"""
        pass
