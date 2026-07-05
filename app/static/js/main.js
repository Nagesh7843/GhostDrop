// File upload and form handling
document.addEventListener('DOMContentLoaded', function() {
    
    // File upload handling
    const fileInput = document.getElementById('file-input');
    const uploadArea = document.getElementById('upload-area');
    const fileNameDisplay = document.getElementById('file-name');
    const fileSizeDisplay = document.getElementById('file-size');
    const fileSelected = document.getElementById('file-selected');
    const uploadForm = document.getElementById('upload-form');
    
    // Expiry mode handling
    const expiryModeRadios = document.querySelectorAll('input[name="expiry_mode"]');
    const timeOptions = document.getElementById('time-options');
    const downloadOptions = document.getElementById('download-options');
    
    let selectedFile = null;
    
    // Click to upload
    if (uploadArea) {
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }
    
    // File selection
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            handleFileSelect(e.target.files[0]);
        });
    }
    
    // Drag and drop
    if (uploadArea) {
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleFileSelect(e.dataTransfer.files[0]);
        });
    }
    
    function handleFileSelect(file) {
        if (!file) return;
        
        selectedFile = file;
        fileNameDisplay.textContent = file.name;
        fileSizeDisplay.textContent = formatFileSize(file.size);
        fileSelected.classList.remove('hidden');
    }
    
    // Expiry mode toggle
    if (expiryModeRadios) {
        expiryModeRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                const mode = e.target.value;
                
                if (timeOptions) timeOptions.classList.add('hidden');
                if (downloadOptions) downloadOptions.classList.add('hidden');
                
                if (mode === 'time' && timeOptions) {
                    timeOptions.classList.remove('hidden');
                } else if (mode === 'download' && downloadOptions) {
                    downloadOptions.classList.remove('hidden');
                }
            });
        });
    }
    
    // Form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!selectedFile) {
                showAlert('Please select a file', 'error');
                return;
            }
            
            const submitBtn = uploadForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading"></span> Uploading...';
            
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('expiry_mode', document.querySelector('input[name="expiry_mode"]:checked').value);
            
            const expiryMode = document.querySelector('input[name="expiry_mode"]:checked').value;
            if (expiryMode === 'time') {
                formData.append('expiry_time', document.getElementById('expiry-time').value);
            } else if (expiryMode === 'download') {
                formData.append('max_downloads', document.getElementById('max-downloads').value);
            }
            
            const password = document.getElementById('password').value;
            if (password) {
                formData.append('password', password);
            }
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showSuccessPage(data);
                } else {
                    showAlert(data.error || 'Upload failed', 'error');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            } catch (error) {
                showAlert('Network error. Please try again.', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        });
    }
    
    // Download handling
    const downloadBtn = document.getElementById('download-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', async () => {
            const code = downloadBtn.dataset.code;
            const passwordInput = document.getElementById('download-password');
            const password = passwordInput ? passwordInput.value : null;
            
            const originalText = downloadBtn.innerHTML;
            downloadBtn.disabled = true;
            downloadBtn.innerHTML = '<span class="loading"></span> Preparing download...';
            
            try {
                const response = await fetch(`/api/download/${code}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ password })
                });
                
                if (response.ok) {
                    // Get filename from header
                    const contentDisposition = response.headers.get('Content-Disposition');
                    let filename = 'download';
                    if (contentDisposition) {
                        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                        if (filenameMatch && filenameMatch[1]) {
                            filename = filenameMatch[1].replace(/['"]/g, '');
                        }
                    }
                    
                    // Download file
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    // Show success message
                    showAlert('Download started successfully!', 'success');
                    
                    // Check if it's one-time download
                    const isOnetime = document.body.dataset.expiry === 'onetime';
                    if (isOnetime) {
                        setTimeout(() => {
                            showAlert('This was a one-time download. The file has been deleted.', 'warning');
                            setTimeout(() => {
                                window.location.href = '/';
                            }, 3000);
                        }, 1000);
                    }
                    
                    downloadBtn.disabled = false;
                    downloadBtn.innerHTML = originalText;
                } else {
                    const data = await response.json();
                    showAlert(data.error || 'Download failed', 'error');
                    downloadBtn.disabled = false;
                    downloadBtn.innerHTML = originalText;
                }
            } catch (error) {
                showAlert('Network error. Please try again.', 'error');
                downloadBtn.disabled = false;
                downloadBtn.innerHTML = originalText;
            }
        });
    }
    
    // Copy to clipboard
    window.copyToClipboard = function(text, button) {
        navigator.clipboard.writeText(text).then(() => {
            const originalText = button.innerHTML;
            button.innerHTML = '✓ Copied!';
            button.classList.add('btn-success');
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
            }, 2000);
        }).catch(() => {
            showAlert('Failed to copy to clipboard', 'error');
        });
    };
    
    // Utility functions
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }
    
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <span>${type === 'success' ? '✓' : type === 'error' ? '✗' : '⚠'}</span>
            <span>${message}</span>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    function showSuccessPage(data) {
        const uploadSection = document.getElementById('upload-section');
        const successSection = document.getElementById('success-section');
        
        document.getElementById('success-code').textContent = data.code;
        document.getElementById('success-filename').textContent = data.filename;
        document.getElementById('success-size').textContent = data.size;
        
        if (data.password_protected) {
            document.getElementById('success-password-notice').classList.remove('hidden');
        }
        
        uploadSection.classList.add('hidden');
        successSection.classList.remove('hidden');
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Download form on homepage
    const downloadForm = document.getElementById('download-form');
    if (downloadForm) {
        downloadForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const code = document.getElementById('code-input').value.trim();
            if (code.length === 6 && /^[0-9]{6}$/.test(code)) {
                window.location.href = '/d/' + code;
            } else {
                showAlert('Please enter a valid 6-digit numeric code', 'error');
            }
        });
        
        // Allow only numeric input
        const codeInput = document.getElementById('code-input');
        if (codeInput) {
            codeInput.addEventListener('input', (e) => {
                // Allow only digits
                e.target.value = e.target.value.replace(/[^0-9]/g, '');
            });
        }
    }
    
});
