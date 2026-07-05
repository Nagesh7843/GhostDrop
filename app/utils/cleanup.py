"""Automatic cleanup of expired files using SQLite backend"""
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.file_handler import FileManager

class CleanupManager:
    """Manages automatic cleanup of expired files"""
    
    def __init__(self, app, db_manager):
        self.app = app
        self.db_manager = db_manager
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
                # Find expired files
                expired_files = self.db_manager.files.get_expired_files()
                
                deleted_count = 0
                for file_doc in expired_files:
                    # Delete physical file
                    file_path = os.path.join(self.upload_folder, file_doc['file_path'])
                    FileManager.delete_file(file_path)
                    
                    # Delete database entry
                    self.db_manager.files.hard_delete_file(file_doc['code'])
                    deleted_count += 1
                
                if deleted_count > 0:
                    print(f"✓ Cleanup: Removed {deleted_count} expired file(s)")
                
                # Also cleanup orphaned files (files without DB entry)
                with self.db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT file_path FROM files')
                    valid_filenames = {row['file_path'] for row in cursor.fetchall()}
                    
                orphaned_count = FileManager.cleanup_orphaned_files(self.upload_folder, valid_filenames)
                
                if orphaned_count > 0:
                    print(f"✓ Cleanup: Removed {orphaned_count} orphaned file(s)")
                    
            except Exception as e:
                print(f"✗ Cleanup error: {e}")
    
    def cleanup_by_code(self, code):
        """Manually cleanup a specific file by code"""
        with self.app.app_context():
            try:
                file_doc = self.db_manager.files.get_file_by_code(code)
                if file_doc:
                    # Delete physical file
                    file_path = os.path.join(self.upload_folder, file_doc['file_path'])
                    FileManager.delete_file(file_path)
                    
                    # Delete database entry
                    self.db_manager.files.hard_delete_file(code)
                    return True, "File deleted successfully"
                return False, "File not found"
            except Exception as e:
                return False, str(e)
