"""Automatic cleanup of expired files"""
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.file_handler import FileManager

class CleanupManager:
    """Manages automatic cleanup of expired files"""
    
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.scheduler = BackgroundScheduler()
        self.upload_folder = app.config['UPLOAD_FOLDER']
    
    def start(self):
        """Start the automatic cleanup scheduler"""
        interval_minutes = self.app.config.get('CLEANUP_INTERVAL_MINUTES', 5)
        
        # Schedule cleanup job
        self.scheduler.add_job(
            func=self.cleanup_expired_files,
            trigger="interval",
            minutes=interval_minutes,
            id='cleanup_expired_files',
            name='Clean up expired files',
            replace_existing=True
        )
        
        self.scheduler.start()
        print(f"✓ Cleanup scheduler started (runs every {interval_minutes} minutes)")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
    
    def cleanup_expired_files(self):
        """Remove expired files from database and filesystem"""
        with self.app.app_context():
            try:
                current_time = datetime.utcnow()
                
                # Find expired files
                expired_files = self.db.files.find({
                    'expires_at': {'$lt': current_time}
                })
                
                deleted_count = 0
                for file_doc in expired_files:
                    # Delete physical file
                    file_path = os.path.join(self.upload_folder, file_doc['file_path'])
                    FileManager.delete_file(file_path)
                    
                    # Delete database entry
                    self.db.files.delete_one({'_id': file_doc['_id']})
                    deleted_count += 1
                
                if deleted_count > 0:
                    print(f"✓ Cleanup: Removed {deleted_count} expired file(s)")
                
                # Also cleanup orphaned files (files without DB entry)
                valid_filenames = {doc['file_path'] for doc in self.db.files.find({}, {'file_path': 1})}
                orphaned_count = FileManager.cleanup_orphaned_files(self.upload_folder, valid_filenames)
                
                if orphaned_count > 0:
                    print(f"✓ Cleanup: Removed {orphaned_count} orphaned file(s)")
                    
            except Exception as e:
                print(f"✗ Cleanup error: {e}")
    
    def cleanup_by_code(self, code):
        """Manually cleanup a specific file by code"""
        with self.app.app_context():
            try:
                file_doc = self.db.files.find_one({'code': code})
                if file_doc:
                    # Delete physical file
                    file_path = os.path.join(self.upload_folder, file_doc['file_path'])
                    FileManager.delete_file(file_path)
                    
                    # Delete database entry
                    self.db.files.delete_one({'code': code})
                    return True, "File deleted successfully"
                return False, "File not found"
            except Exception as e:
                return False, str(e)
