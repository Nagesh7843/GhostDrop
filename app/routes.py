"""Flask routes for GhostDrop"""
import os
from datetime import timedelta
from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.exceptions import RequestEntityTooLarge
from app.utils import SecurityManager, FileManager
from app.models import FileModel

main_bp = Blueprint('main', __name__)

def get_client_ip():
    """Get client IP address (handles proxies)"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr


@main_bp.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@main_bp.route('/upload', methods=['GET'])
def upload_page():
    """Upload page"""
    expiry_options = current_app.config['EXPIRY_OPTIONS']
    return render_template('upload.html', expiry_options=expiry_options)


@main_bp.route('/api/upload', methods=['POST'])
def api_upload():
    """Handle file upload"""
    
    # Rate limiting check
    rate_limiter = current_app.config['RATE_LIMITER']
    client_ip = get_client_ip()
    max_requests = current_app.config['MAX_REQUESTS_PER_MINUTE']
    
    if not rate_limiter.is_allowed(client_ip, max_requests):
        return jsonify({
            'success': False,
            'error': 'Rate limit exceeded. Please wait before uploading again.'
        }), 429
    
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Get form data
    expiry_mode = request.form.get('expiry_mode', 'onetime')
    expiry_time = request.form.get('expiry_time', '1day')
    max_downloads = request.form.get('max_downloads', None)
    password = request.form.get('password', None)
    
    # Validate file extension
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    if not SecurityManager.validate_file_extension(file.filename, allowed_extensions):
        return jsonify({
            'success': False,
            'error': 'File type not allowed'
        }), 400
    
    # Securely save file
    upload_folder = current_app.config['UPLOAD_FOLDER']
    FileManager.ensure_upload_folder(upload_folder)
    
    success, filename, error = SecurityManager.secure_file_save(file, upload_folder)
    if not success:
        return jsonify({'success': False, 'error': error}), 400
    
    # Get file size
    file_path = os.path.join(upload_folder, filename)
    file_size = FileManager.get_file_size(file_path)
    
    # Generate secure code
    code = SecurityManager.generate_secure_token(current_app.config['TOKEN_LENGTH'])
    
    # Handle password
    password_hash = None
    if password and len(password.strip()) > 0:
        if len(password) < current_app.config['PASSWORD_MIN_LENGTH']:
            FileManager.delete_file(file_path)
            return jsonify({
                'success': False,
                'error': f"Password must be at least {current_app.config['PASSWORD_MIN_LENGTH']} characters"
            }), 400
        password_hash = SecurityManager.hash_password(password)
    
    # Determine expiry
    db_manager = current_app.config['DB_MANAGER']
    
    if expiry_mode == 'onetime':
        # One-time download
        success, result = db_manager.files.create_file_entry(
            code=code,
            filename=filename,
            file_path=filename,
            file_size=file_size,
            expiry_type='onetime',
            expiry_value=timedelta(days=7),
            max_downloads=1,
            password_hash=password_hash,
            original_filename=file.filename
        )
    elif expiry_mode == 'time':
        # Time-based expiry
        expiry_options = current_app.config['EXPIRY_OPTIONS']
        expiry_delta = expiry_options.get(expiry_time, timedelta(days=1))
        
        success, result = db_manager.files.create_file_entry(
            code=code,
            filename=filename,
            file_path=filename,
            file_size=file_size,
            expiry_type='time',
            expiry_value=expiry_delta,
            password_hash=password_hash,
            original_filename=file.filename
        )
    elif expiry_mode == 'download':
        # Download-limit based expiry
        try:
            max_downloads_int = int(max_downloads) if max_downloads else 5
            max_downloads_int = max(1, min(max_downloads_int, 100))  # Limit between 1-100
        except:
            max_downloads_int = 5
        
        success, result = db_manager.files.create_file_entry(
            code=code,
            filename=filename,
            file_path=filename,
            file_size=file_size,
            expiry_type='download',
            expiry_value=timedelta(days=30),
            max_downloads=max_downloads_int,
            password_hash=password_hash,
            original_filename=file.filename
        )
    else:
        FileManager.delete_file(file_path)
        return jsonify({'success': False, 'error': 'Invalid expiry mode'}), 400
    
    if not success:
        FileManager.delete_file(file_path)
        return jsonify({'success': False, 'error': str(result)}), 500
    
    return jsonify({
        'success': True,
        'code': code,
        'filename': file.filename,
        'size': FileManager.get_file_size_human_readable(file_size),
        'password_protected': password_hash is not None
    }), 200


@main_bp.route('/d/<code>')
def download_page(code):
    """Download page - shows file info and download button"""
    code = SecurityManager.sanitize_input(code, max_length=6)
    
    db_manager = current_app.config['DB_MANAGER']
    file_doc = db_manager.files.get_file_by_code(code)
    
    if not file_doc:
        return render_template('error.html', 
                             error='File not found',
                             message='This file does not exist or has been deleted.'), 404
    
    # Check if expired
    from datetime import datetime
    if file_doc['expires_at'] < datetime.utcnow():
        return render_template('error.html',
                             error='File expired',
                             message='This file has expired and is no longer available.'), 410
    
    # Check if download limit reached
    if file_doc.get('max_downloads'):
        if file_doc['current_downloads'] >= file_doc['max_downloads']:
            return render_template('error.html',
                                 error='Download limit reached',
                                 message='This file has reached its maximum download limit.'), 410
    
    return render_template('download.html', 
                         code=code,
                         file=file_doc)


@main_bp.route('/api/download/<code>', methods=['POST'])
def api_download(code):
    """Handle file download with optional password"""
    code = SecurityManager.sanitize_input(code, max_length=6)
    
    # Get password if provided
    data = request.get_json() or {}
    password = data.get('password', None)
    
    db_manager = current_app.config['DB_MANAGER']
    file_doc = db_manager.files.get_file_by_code(code)
    
    if not file_doc:
        return jsonify({'success': False, 'error': 'File not found'}), 404
    
    # Check password
    if file_doc['password_protected']:
        if not password:
            return jsonify({'success': False, 'error': 'Password required'}), 401
        
        if not SecurityManager.verify_password(password, file_doc['password_hash']):
            return jsonify({'success': False, 'error': 'Invalid password'}), 401
    
    # Check if expired
    from datetime import datetime
    if file_doc['expires_at'] < datetime.utcnow():
        return jsonify({'success': False, 'error': 'File expired'}), 410
    
    # Increment download count
    file_doc, status = db_manager.files.increment_download_count(code)
    
    if file_doc is None:
        return jsonify({'success': False, 'error': status}), 404
    
    # Get file path
    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, file_doc['file_path'])
    
    if not FileManager.file_exists(file_path):
        return jsonify({'success': False, 'error': 'File not found on server'}), 404
    
    # If download limit reached, schedule deletion
    should_delete = False
    if status == "DELETE":
        should_delete = True
    
    # Send file
    try:
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=file_doc['original_filename']
        )
        
        # If should delete, mark for cleanup
        if should_delete:
            # The cleanup scheduler will handle actual deletion
            db_manager.files.delete_file(code)
        
        return response
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main_bp.route('/api/stats')
def api_stats():
    """Get system statistics (admin only in production)"""
    db_manager = current_app.config['DB_MANAGER']
    stats = db_manager.files.get_stats()
    return jsonify(stats)


@main_bp.errorhandler(413)
@main_bp.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle file size too large error"""
    max_size = current_app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
    return jsonify({
        'success': False,
        'error': f'File too large. Maximum size is {max_size:.0f}MB'
    }), 413


@main_bp.errorhandler(404)
def handle_404(e):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Not found'}), 404
    return render_template('error.html', 
                         error='404 - Not Found',
                         message='The page you are looking for does not exist.'), 404


@main_bp.errorhandler(500)
def handle_500(e):
    """Handle 500 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    return render_template('error.html',
                         error='500 - Server Error',
                         message='Something went wrong. Please try again later.'), 500
