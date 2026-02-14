# Quick Setup Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Python & MongoDB

**Windows:**
```bash
# Install Python from python.org
# Install MongoDB Community Server from mongodb.com
```

### 2. Setup Project

```bash
# Clone or download the project
cd file_sharingwebapp

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env
```

### 3. Start MongoDB

```bash
# If installed as Windows service
net start MongoDB

# Or run manually
mongod
```

### 4. Run GhostDrop

```bash
python run.py
```

### 5. Open Browser

Visit: **http://localhost:5000**

---

## ✅ That's it!

You now have GhostDrop running locally.

### Next Steps:

- Upload a test file
- Try different expiry modes
- Test password protection
- Read DEPLOYMENT.md for production setup

---

## 🐳 Or Use Docker (Even Easier!)

```bash
docker-compose up -d
```

Done! Visit http://localhost:5000

---

## ⚙️ Configuration

Edit `.env` file to customize:

```
SECRET_KEY=your-secret-key
MAX_CONTENT_LENGTH=52428800  # 50MB
MAX_REQUESTS_PER_MINUTE=10
```

---

## 📚 Documentation

- **README.md** - Full documentation
- **DEPLOYMENT.md** - Production deployment guide
- **config.py** - Configuration options

---

## 🆘 Troubleshooting

**MongoDB not connecting?**
```bash
# Check if MongoDB is running
mongosh

# If not, start it
net start MongoDB
```

**Port 5000 already in use?**
```bash
# Edit .env and change PORT=5001
```

**Module not found?**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

**Happy file sharing! 👻**
