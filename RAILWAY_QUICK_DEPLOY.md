# 🚂 Railway Quick Deploy

## Copy-Paste Environment Variables

Add these in Railway **Variables** tab:

### Variable 1: MONGODB_URI
```
mongodb+srv://gnagesh550_db_user:nagesh7843@cluster0.j1i5ch9.mongodb.net/ghostdrop?retryWrites=false&w=majority&authSource=admin&tlsAllowInvalidCertificates=true
```

### Variable 2: SECRET_KEY
Generate from: https://randomkeygen.com (copy a Fort Knox password)

### Variable 3: FLASK_ENV
```
production
```

### Variable 4: DEBUG
```
False
```

### Variable 5: MONGODB_DB_NAME
```
ghostdrop
```

### Variable 6: PORT
```
5000
```

---

## Deployment Fixed Issues

✅ **Worker timeout** - Reduced to 1 worker (free tier friendly)  
✅ **MongoDB connection** - Faster timeout (10s instead of 30s)  
✅ **Startup blocking** - Silent index creation  
✅ **Memory issues** - Single worker with more threads  

---

## Railway vs Render

| Issue | Render | Railway |
|-------|--------|---------|
| Deployment speed | 🐌 5-10 min | ⚡ 2-3 min |
| Worker timeouts | ❌ Frequent | ✅ Rare |
| Auto-deploy | ⏳ Slow | ⚡ Fast |
| Free tier | 750 hrs | $5 credit |
| Build reliability | ❌ Issues | ✅ Stable |

---

## Deploy Now

1. **https://railway.app** → Login with GitHub
2. **New Project** → Deploy from GitHub repo
3. Select **GhostDrop**
4. Add **6 environment variables** above
5. **Generate Domain** in Settings → Networking
6. **Done!** Your app will be live in 2-3 minutes

---

## After Deployment

Check deployment logs for:
```
✓ Connected to MongoDB
✓ Cleanup scheduler started
✓ GhostDrop initialized
Listening at: http://0.0.0.0:5000
```

**Then visit your Railway URL and test file upload!** 🎉
