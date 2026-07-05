"""Security utilities for GhostDrop"""
import secrets
import string
import bcrypt
import mimetypes
import os
from werkzeug.utils import secure_filename

class SecurityManager:
    """Handles all security-related operations"""
    
    @staticmethod
    def generate_secure_token(length=6):
        """
        Generate a cryptographically secure random token
        Uses only digits (0-9) for easy sharing
        """
        alphabet = string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt"""
        if not password:
            return None
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verify a password against its hash"""
        if not password or not password_hash:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash)
        except Exception:
            return False
    
    @staticmethod
    def validate_file_extension(filename, allowed_extensions):
        """Check if file has an allowed extension"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def validate_mime_type(file_path):
        """
        Validate file MIME type to prevent malicious uploads
        Returns (is_valid, mime_type)
        """
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # List of potentially dangerous MIME types to block
        dangerous_types = [
            'application/x-msdownload',  # .exe
            'application/x-msdos-program',
            'application/x-sh',  # shell scripts
            'application/x-bat',  # batch files
            'text/x-shellscript',
        ]
        
        if mime_type in dangerous_types:
            return False, mime_type
        
        return True, mime_type
    
    @staticmethod
    def secure_file_save(file, upload_folder):
        """
        Securely save uploaded file with sanitized filename
        Returns (success, filename, error_message)
        """
        try:
            # Get secure filename
            original_filename = secure_filename(file.filename)
            
            # Generate unique filename to prevent conflicts
            base_name, extension = os.path.splitext(original_filename)
            unique_filename = f"{base_name}_{secrets.token_hex(8)}{extension}"
            
            # Full path
            file_path = os.path.join(upload_folder, unique_filename)
            
            # Save file
            file.save(file_path)
            
            # Validate MIME type after saving
            is_valid, mime_type = SecurityManager.validate_mime_type(file_path)
            if not is_valid:
                os.remove(file_path)
                return False, None, f"File type not allowed: {mime_type}"
            
            return True, unique_filename, None
            
        except Exception as e:
            return False, None, str(e)
    
    @staticmethod
    def sanitize_input(text, max_length=500):
        """Sanitize user input to prevent injection attacks"""
        if not text:
            return ""
        # Remove potentially dangerous characters
        text = text.strip()
        text = text[:max_length]
        return text


class RateLimiter:
    """Simple in-memory rate limiter (use Redis in production for distributed systems)"""
    
    def __init__(self):
        self.requests = {}  # {ip: [timestamps]}
    
    def is_allowed(self, ip_address, max_requests, time_window_seconds=60):
        """
        Check if request from IP is allowed
        Args:
            ip_address: Client IP
            max_requests: Maximum requests allowed
            time_window_seconds: Time window in seconds
        """
        import time
        current_time = time.time()
        
        # Clean old entries
        if ip_address in self.requests:
            self.requests[ip_address] = [
                ts for ts in self.requests[ip_address] 
                if current_time - ts < time_window_seconds
            ]
        else:
            self.requests[ip_address] = []
        
        # Check limit
        if len(self.requests[ip_address]) >= max_requests:
            return False
        
        # Add current request
        self.requests[ip_address].append(current_time)
        return True
    
    def cleanup_old_entries(self, max_age_seconds=3600):
        """Remove entries older than max_age_seconds"""
        import time
        current_time = time.time()
        
        for ip in list(self.requests.keys()):
            self.requests[ip] = [
                ts for ts in self.requests[ip]
                if current_time - ts < max_age_seconds
            ]
            if not self.requests[ip]:
                del self.requests[ip]
