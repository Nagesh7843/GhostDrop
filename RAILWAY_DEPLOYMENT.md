# 🚂 Railway Deployment Guide

## Why Railway?
✅ Easier than Render  
✅ Auto-deploys from GitHub  
✅ $5 free credit monthly  
✅ Better reliability  

---

## 🚀 Deploy in 5 Minutes

### Step 1: Create Railway Account
1. Go to: **https://railway.app**
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway to access your GitHub

---

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **"GhostDrop"** repository
4. Click **"Deploy Now"**

Railway will automatically:
- ✅ Detect your Dockerfile
- ✅ Build the Docker image
- ✅ Start deployment

---

### Step 3: Add Environment Variables
1. Click on your deployed service
2. Go to **"Variables"** tab
3. Click **"New Variable"** for each:

```
MONGODB_URI=mongodb+srv://gnagesh550_db_user:nagesh7843@cluster0.j1i5ch9.mongodb.net/ghostdrop?retryWrites=false&w=majority&authSource=admin&tlsAllowInvalidCertificates=true
```

```
SECRET_KEY=(generate from https://randomkeygen.com)
```

```
FLASK_ENV=production
```

```
DEBUG=False
```

```
MONGODB_DB_NAME=ghostdrop
```

```
PORT=5000
```

---

### Step 4: Get Your URL
1. Go to **"Settings"** tab
2. Scroll to **"Networking"**
3. Click **"Generate Domain"**
4. You'll get: `your-app.up.railway.app`

**That's your live URL!** 🎉

---

## 🧪 Test Your Deployment

1. Visit your Railway URL
2. Upload a test file
3. Get the 6-digit code
4. Download the file using the code

---

## 📊 Monitor Your App

**Railway Dashboard:**
- **Deployments** - See build logs
- **Metrics** - CPU/Memory usage
- **Logs** - Real-time app logs

**Check if running:**
- Look for: `✓ Connected to MongoDB`
- Look for: `Running on http://0.0.0.0:5000`

---

## 💰 Free Tier Limits

- **$5 credit/month** (renews monthly)
- **~500 hours** of runtime
- **~20GB** bandwidth
- **Unlimited** deployments

**Perfect for GhostDrop!**

---

## 🔧 Automatic Deployments

Railway auto-deploys when you push to GitHub:

```powershell
git add .
git commit -m "Update feature"
git push origin main
```

Railway will automatically rebuild and redeploy! ✨

---

## 🆘 Troubleshooting

### Deployment Failed?
1. Check **Deployments** tab for errors
2. Common issues:
   - ❌ Missing environment variables
   - ❌ MongoDB connection (check IP whitelist: 0.0.0.0/0)
   - ❌ Wrong MongoDB credentials

### Can't Access URL?
1. Make sure domain is generated in Settings → Networking
2. Check if deployment shows "Active"
3. View logs for errors

### MongoDB Connection Issues?
1. Go to MongoDB Atlas
2. Network Access → Add IP: `0.0.0.0/0` (allow all)
3. Database Access → Verify user: `gnagesh550_db_user`

---

## ✨ Advantages Over Render

| Feature | Railway | Render |
|---------|---------|--------|
| Setup Time | 2 minutes | 5+ minutes |
| Auto-deploy | ✅ Instant | ⏳ Slower |
| Logs | Real-time | Delayed |
| Free tier | $5/month | 750 hrs |
| Build speed | ⚡ Fast | 🐌 Slow |

---

## 🎯 Next Steps After Deployment

1. ✅ Verify app works at Railway URL
2. 🔗 Share URL with testers
3. 📊 Monitor usage in Railway dashboard
4. 🔄 Push updates to GitHub (auto-deploys)

---

**Ready to deploy? Go to https://railway.app now!** 🚂
