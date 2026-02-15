# 🎯 Render Deployment - Complete Setup

## Current Status
✅ Code pushed with fixes for:
- Worker timeout issues (now 1 worker instead of 4)
- MongoDB connection timeouts (10s faster detection)
- Index creation (non-blocking)
- Graceful shutdown (30s grace period)

---

## Step 1: Check Render Dashboard
Go to: **https://dashboard.render.com**

1. Click **"GhostDrop"** service
2. Click **"Settings"** tab
3. Look for **"Environment"** section

---

## Step 2: Add Environment Variables

In the **"Environment"** section, add these 6 variables:

### Variable 1: MONGODB_URI
```
mongodb+srv://gnagesh550_db_user:nagesh7843@cluster0.j1i5ch9.mongodb.net/ghostdrop?retryWrites=false&w=majority&authSource=admin&tlsAllowInvalidCertificates=true
```

### Variable 2: SECRET_KEY
Generate from: **https://randomkeygen.com**
(Copy any of the long "Fort Knox" passwords)

Example:
```
eK9mX@2qL#5nR$7vB%3jQ&wE^4tY(8uI)0oA-sD+fG*hJ=lK[pO{mN}
```

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

## Step 3: Save and Redeploy

1. After adding all 6 variables, click **"Save Changes"**
2. Render will automatically redeploy
3. Check **"Deployments"** tab to see progress
4. **Wait 3-5 minutes** for deployment to complete

---

## Step 4: Check Logs

In **"Logs"** tab, you should see:

```
✓ Connected to MongoDB
✓ Cleanup scheduler started (runs every 5 minutes)
✓ GhostDrop initialized
...
Listening at: http://0.0.0.0:5000
```

If you see errors, check:
- ❌ `MongoDB connection error` → Check if IP whitelist is `0.0.0.0/0` in MongoDB Atlas
- ❌ `index creation` → Normal warning, can ignore
- ❌ `Worker timeout` → Already fixed in latest code

---

## Step 5: Test Your App

Once deployed, visit: **https://ghostdrop-rqiz.onrender.com**

1. Upload a test file
2. You should get a **6-digit code** (e.g., 482917)
3. Close the browser
4. Enter the code to download the file

---

## Troubleshooting Render Issues

### Issue: Still getting "502 Bad Gateway"
**Solution:**
1. Check Logs for actual error messages
2. Verify all 6 environment variables are added
3. Click **"Manual Deploy"** to trigger new build

### Issue: "MongoDB connection timeout"
**Solution:**
1. Go to MongoDB Atlas: https://cloud.mongodb.com
2. Network Access → Edit IP Whitelist
3. Make sure `0.0.0.0/0` is added (allow all IPs)
4. Wait 2-3 minutes for change to apply

### Issue: "Could not create indexes"
**Solution:**
- This is OK - it's now silent and non-blocking
- App will still work

### Issue: "Worker timeout" errors
**Solution:**
- Already fixed in latest code!
- If still happening, wait for Render's redeploy to complete (5+ minutes)

---

## Expected Timeline

| Step | Time |
|------|------|
| Add env variables | Now |
| Render rebuilds | 3-5 min |
| Build completes | 5-8 min |
| App comes online | 8-10 min |
| **App ready to use** | **~10 minutes** |

---

## Your Live URL
```
https://ghostdrop-rqiz.onrender.com
```

---

## ✅ Checklist Before Render Redeploy

- [ ] All 6 environment variables added
- [ ] MongoDB Atlas IP whitelist includes `0.0.0.0/0`
- [ ] GitHub shows latest commit (fde91ff with worker fixes)
- [ ] Render service shows "Deploy" option

---

## Next Steps

1. Add the 6 environment variables now
2. Wait for Render to redeploy (10 min)
3. Visit `https://ghostdrop-rqiz.onrender.com`
4. Test file upload → Get 6-digit code → Download file

**Your app will be live!** 🚀
