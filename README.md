# GhostDrop - Temporary File Sharing

![GhostDrop](https://img.shields.io/badge/GhostDrop-Privacy%20First-6366f1)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-brightgreen)

**GhostDrop** is a privacy-first, temporary file sharing application with no login required. Files are automatically deleted after expiry, ensuring no permanent trace.

## 🔥 Features

- **No Account Required** - Upload and share files instantly
- **Simple 6-Digit Numeric Codes** - Easy to share and remember (e.g., 123456)
- **Enter Code on Same Page** - No URLs, just enter the code on homepage
- **Multiple Expiry Modes**:
  - 🔥 One-time download (auto-delete after first download)
  - ⏳ Time-based expiry (1 hour to 7 days)
  - 📉 Download-limited expiry (1-100 downloads)
- **Password Protection** - Optional password for files
- **Auto Cleanup** - Scheduled deletion of expired files
- **Rate Limiting** - IP-based rate limiting for security
- **File Validation** - MIME type checking and size limits
- **Privacy First** - No tracking, no logging, no permanent storage

## 🏗️ Architecture

**Backend:**
- Flask (Python web framework)
- MongoDB (document database)
- APScheduler (automatic cleanup)
- bcrypt (password hashing)
- Werkzeug (secure file handling)

**Frontend:**
- Vanilla JavaScript (no frameworks)
- Modern CSS with dark theme
- Responsive design

**Security:**
- Secure token generation using `secrets` module
- Password hashing with bcrypt
- File type validation
- Rate limiting
- File size restrictions (50MB default)

## 📦 Installation

### Option 1: Docker (Recommended)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd file_sharingwebapp
```

2. **Create environment file**
```bash
cp .env.example .env
```

Edit `.env` and set a strong secret key:
```
SECRET_KEY=your-super-secret-key-here-change-this
```

3. **Run with Docker Compose**
```bash
docker-compose up -d
```

The app will be available at `http://localhost:5000`

### Option 2: Local Development

1. **Prerequisites**
   - Python 3.11+
   - MongoDB 7.0+

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Start MongoDB**
```bash
# On Windows
mongod

# On Linux/Mac
sudo systemctl start mongodb
```

5. **Run the application**
```bash
python run.py
```

Visit `http://localhost:5000`

## 🚀 Deployment

### Deploy to Render / Railway / DigitalOcean

1. **Set environment variables:**
   - `SECRET_KEY` - Strong random key
   - `MONGODB_URI` - MongoDB connection string
   - `FLASK_ENV=production`
   - `MAX_CONTENT_LENGTH` - Max file size in bytes

2. **Use Dockerfile for deployment**

3. **Enable HTTPS** (handled by platform)

### Deploy to VPS (Ubuntu)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone and deploy
git clone <your-repo>
cd file_sharingwebapp
docker-compose up -d

# Setup nginx reverse proxy for HTTPS
# (Optional but recommended)
```

## 🔒 Security Features

✅ Cryptographically secure 6-digit code generation  
✅ Rate limiting (10 requests/minute per IP)  
✅ File size limits (50MB default)  
✅ MIME type validation  
✅ Password hashing with bcrypt  
✅ Automatic file deletion  
✅ No logging of file contents  
✅ No tracking of users  

## 📊 Database Schema

```javascript
{
  code: "482917",                    // 6-digit numeric code
  file_path: "file_abc123.pdf",  // Stored filename
  original_filename: "doc.pdf",   // Original filename
  file_size: 1048576,             // Size in bytes
  file_size_human: "1.00 MB",     // Human readable
  expiry_type: "onetime",         // onetime | time | download
  created_at: ISODate(),          // Upload time
  expires_at: ISODate(),          // Expiry time
  max_downloads: 1,               // Max downloads (if applicable)
  current_downloads: 0,           // Current download count
  password_protected: false,      // Has password?
  password_hash: null,            // Hashed password
  deleted: false                  // Soft delete flag
}
```

## 🛠️ Configuration

Edit `config.py` to customize:

- `MAX_CONTENT_LENGTH` - Maximum file size
- `TOKEN_LENGTH` - Length of access codes (6-digits)
- `MAX_REQUESTS_PER_MINUTE` - Rate limit
- `CLEANUP_INTERVAL_MINUTES` - How often to run cleanup
- `EXPIRY_OPTIONS` - Available expiry time options
- `ALLOWED_EXTENSIONS` - Permitted file types

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/upload` | GET | Upload form |
| `/api/upload` | POST | Handle file upload |
| `/d/<code>` | GET | Download page |
| `/api/download/<code>` | POST | Download file |
| `/api/stats` | GET | System statistics |

## 📈 Future Enhancements

- [ ] End-to-end encryption (client-side)
- [ ] QR code generation for links
- [ ] LAN-only mode for local transfers
- [ ] File preview for images/PDFs
- [ ] Audit logs for enterprise version
- [ ] S3/cloud storage integration
- [ ] API tokens for programmatic access
- [ ] Multi-file upload (ZIP)
- [ ] Custom expiry times
- [ ] Admin dashboard

## 🤝 Contributing

This is a learning project. Feel free to fork, modify, and learn from it!

## 📝 License

MIT License - Use freely for personal and commercial projects.

## ⚠️ Disclaimer

This is a file sharing tool. Users are responsible for the content they upload. Do not use for illegal activities.

## 🎓 Learning Outcomes

Building this project teaches:
- Backend API design
- Database modeling
- Security best practices
- File handling in web apps
- Scheduled tasks
- Docker containerization
- Production deployment

---

**Made with 🧠 for learning system design and security**
