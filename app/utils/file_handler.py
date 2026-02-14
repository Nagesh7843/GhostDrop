"""File handling utilities"""
import os
import shutil
from datetime import datetime

class FileManager:
    """Handles file operations"""
    
    @staticmethod
    def get_file_size(file_path):
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    @staticmethod
    def get_file_size_human_readable(size_bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    @staticmethod
    def delete_file(file_path):
        """Safely delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True, "File deleted successfully"
        except Exception as e:
            return False, f"Error deleting file: {str(e)}"
        return False, "File not found"
    
    @staticmethod
    def file_exists(file_path):
        """Check if file exists"""
        return os.path.exists(file_path)
    
    @staticmethod
    def ensure_upload_folder(upload_folder):
        """Ensure upload folder exists"""
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)
    
    @staticmethod
    def get_file_age_hours(file_path):
        """Get file age in hours"""
        try:
            created_time = os.path.getctime(file_path)
            age_seconds = datetime.now().timestamp() - created_time
            return age_seconds / 3600
        except:
            return 0
    
    @staticmethod
    def cleanup_orphaned_files(upload_folder, valid_filenames):
        """
        Remove files that are not in the database
        Args:
            upload_folder: Path to uploads folder
            valid_filenames: Set of filenames that should exist
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        try:
            if not os.path.exists(upload_folder):
                return 0
            
            for filename in os.listdir(upload_folder):
                if filename == '.gitkeep':
                    continue
                    
                if filename not in valid_filenames:
                    file_path = os.path.join(upload_folder, filename)
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error deleting orphaned file {filename}: {e}")
        except Exception as e:
            print(f"Error during orphaned file cleanup: {e}")
        
        return deleted_count
