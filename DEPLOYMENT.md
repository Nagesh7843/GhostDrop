# GhostDrop Deployment Guide

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- MongoDB 7.0+

### Setup Steps

1. **Install MongoDB**

Windows:
```bash
# Download from https://www.mongodb.com/try/download/community
# Or use chocolatey:
choco install mongodb
```

2. **Install Python Dependencies**
```bash
pip install -r requirements.txt
```

3. **Create Environment File**
```bash
cp .env.example .env
```

Edit `.env`:
```
SECRET_KEY=dev-secret-key-for-testing
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=ghostdrop
```

4. **Start MongoDB**
```bash
# Windows (if installed as service)
net start MongoDB

# Or run manually
mongod --dbpath C:\data\db
```

5. **Run the Application**
```bash
python run.py
```

Visit: `http://localhost:5000`

---

## 🐳 Docker Deployment (Production)

### Local Docker Setup

1. **Install Docker Desktop**
   - Windows: https://www.docker.com/products/docker-desktop
   - Ensure WSL2 is enabled

2. **Configure Environment**
```bash
cp .env.example .env
```

Edit `.env` with production settings:
```
SECRET_KEY=your-super-secret-production-key-here
DEBUG=False
MONGODB_URI=mongodb://mongodb:27017/
MONGODB_DB_NAME=ghostdrop
MAX_REQUESTS_PER_MINUTE=10
```

3. **Build and Run**
```bash
docker-compose up --build -d
```

4. **Check Status**
```bash
docker-compose ps
docker-compose logs -f app
```

5. **Stop**
```bash
docker-compose down
```

---

## ☁️ Deploy to Cloud Platforms

### Option 1: Render.com (Free Tier Available)

1. **Create account at render.com**

2. **Create Web Service**
   - Connect your GitHub repo
   - Select "Docker"
   - Environment: Production

3. **Add Environment Variables**
```
SECRET_KEY=<generate-random-key>
FLASK_ENV=production
MONGODB_URI=<your-mongodb-atlas-uri>
MONGODB_DB_NAME=ghostdrop
MAX_CONTENT_LENGTH=52428800
```

4. **Create MongoDB Atlas Database**
   - Sign up at mongodb.com/atlas
   - Create free cluster
   - Get connection string
   - Whitelist all IPs (0.0.0.0/0)

5. **Deploy**
   - Render will auto-build and deploy
   - Access via provided URL

### Option 2: Railway.app

1. **Install Railway CLI**
```bash
npm i -g @railway/cli
railway login
```

2. **Deploy**
```bash
railway init
railway up
```

3. **Add MongoDB**
```bash
railway add mongodb
```

4. **Set Environment Variables**
```bash
railway variables set SECRET_KEY=<your-key>
railway variables set FLASK_ENV=production
```

### Option 3: DigitalOcean (VPS)

1. **Create Droplet**
   - Ubuntu 22.04 LTS
   - 1GB RAM minimum
   - Enable SSH access

2. **Connect to Server**
```bash
ssh root@your-server-ip
```

3. **Install Dependencies**
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y
```

4. **Clone Repository**
```bash
git clone <your-repo-url>
cd file_sharingwebapp
```

5. **Configure Environment**
```bash
nano .env
# Add your production settings
```

6. **Deploy**
```bash
docker-compose up -d
```

7. **Setup Nginx Reverse Proxy (Optional but Recommended)**
```bash
apt install nginx certbot python3-certbot-nginx -y

# Create nginx config
nano /etc/nginx/sites-available/ghostdrop
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 50M;
    }
}
```

Enable and restart:
```bash
ln -s /etc/nginx/sites-available/ghostdrop /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Get SSL certificate
certbot --nginx -d your-domain.com
```

---

## 🔒 Production Security Checklist

- [ ] Change SECRET_KEY to random value
- [ ] Set DEBUG=False
- [ ] Use HTTPS (SSL certificate)
- [ ] Enable firewall (only open 80, 443, 22)
- [ ] Restrict MongoDB access
- [ ] Use environment variables (never hardcode)
- [ ] Set up monitoring/logging
- [ ] Regular backups of MongoDB
- [ ] Keep dependencies updated
- [ ] Set up rate limiting at nginx level
- [ ] Use strong MongoDB credentials

---

## 📊 Monitoring

### Check Application Logs
```bash
# Docker
docker-compose logs -f app

# Direct
tail -f /path/to/logs
```

### MongoDB Statistics
```bash
docker exec -it ghostdrop-mongodb mongosh

# In MongoDB shell
use ghostdrop
db.files.countDocuments()
db.files.find({deleted: false}).count()
```

### System Health
```bash
# Check disk space
df -h

# Check memory
free -h

# Check running processes
docker ps
```

---

## 🔧 Maintenance

### Update Application
```bash
git pull origin main
docker-compose down
docker-compose up --build -d
```

### Clear Old Files Manually
```bash
# Access MongoDB
docker exec -it ghostdrop-mongodb mongosh ghostdrop

# Delete expired files
db.files.deleteMany({expires_at: {$lt: new Date()}})
```

### Backup Database
```bash
docker exec ghostdrop-mongodb mongodump --out=/data/backup
docker cp ghostdrop-mongodb:/data/backup ./mongo-backup
```

### Restore Database
```bash
docker cp ./mongo-backup ghostdrop-mongodb:/data/restore
docker exec ghostdrop-mongodb mongorestore /data/restore
```

---

## 🐛 Troubleshooting

### MongoDB Connection Failed
```bash
# Check MongoDB is running
docker ps | grep mongodb

# Check logs
docker logs ghostdrop-mongodb

# Test connection
docker exec -it ghostdrop-mongodb mongosh
```

### File Upload Fails
- Check disk space: `df -h`
- Check upload folder permissions
- Verify MAX_CONTENT_LENGTH setting
- Check nginx client_max_body_size

### App Won't Start
```bash
# Check logs
docker-compose logs app

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Rate Limit Issues
- Adjust MAX_REQUESTS_PER_MINUTE in config
- Check IP forwarding in nginx
- Clear rate limiter (restart app)

---

## 📞 Support

For issues and questions:
1. Check logs first
2. Review configuration
3. Search existing issues on GitHub
4. Create new issue with:
   - Error logs
   - Environment details
   - Steps to reproduce

---

**Remember:** This is a learning project. Use in production at your own risk. Always test thoroughly before deploying.
