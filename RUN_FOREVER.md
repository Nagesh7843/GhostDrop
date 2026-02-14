# 🚀 How to Run GhostDrop Permanently

## ✅ **Quickest Method - Windows Task Scheduler** (Recommended)

This will make GhostDrop start automatically when Windows boots and keep running forever.

### **Step-by-Step Guide:**

#### 1. **Open Task Scheduler**
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

#### 2. **Create New Task**
   - Click **"Create Task..."** (right panel)
   - **DO NOT** use "Create Basic Task" - use "Create Task"

#### 3. **General Tab:**
   - Name: `GhostDrop Server`
   - Description: `File sharing web application`
   - ✅ Check: **"Run whether user is logged on or not"**
   - ✅ Check: **"Run with highest privileges"**
   - Configure for: **Windows 10** (or your Windows version)

#### 4. **Triggers Tab:**
   - Click **"New..."**
   - Begin the task: **"At startup"**
   - Delay task for: **30 seconds** (optional, gives Windows time to start)
   - Click **OK**

#### 5. **Actions Tab:**
   - Click **"New..."**
   - Action: **"Start a program"**
   - Program/script: 
     ```
     C:\Users\n2005\file sharingwebapp\.venv\Scripts\python.exe
     ```
   - Add arguments:
     ```
     run_production.py
     ```
   - Start in:
     ```
     C:\Users\n2005\file sharingwebapp
     ```
   - Click **OK**

#### 6. **Conditions Tab:**
   - ❌ **Uncheck**: "Start the task only if the computer is on AC power"
   - ❌ **Uncheck**: "Stop if the computer switches to battery power"

#### 7. **Settings Tab:**
   - ✅ Check: **"Allow task to be run on demand"**
   - ✅ Check: **"If the task fails, restart every: 1 minute"**
   - Set attempts to restart: **3**
   - ✅ Check: **"Stop the task if it runs longer than: 3 days"** → Change to **"Do not stop"**

#### 8. **Save**
   - Click **OK**
   - Enter your **Windows password** when prompted

---

## ✅ **Test It Right Now**

### **Manual Start (Test First):**

```powershell
# Open PowerShell in project folder
cd C:\Users\n2005\file sharingwebapp

# Run production server
& "C:\Users\n2005\file sharingwebapp\.venv\Scripts\python.exe" run_production.py
```

You should see:
```
============================================================
🚀 GhostDrop Production Server
============================================================
Environment: production
Running on: http://0.0.0.0:5000
Press Ctrl+C to stop
============================================================
```

**Open browser:** http://localhost:5000

---

## ✅ **Or Use the Batch File (Even Easier)**

### **Option A: Double-Click to Start**
Just double-click: `start_production.bat`

### **Option B: Add to Windows Startup**
1. Press `Win + R`
2. Type: `shell:startup`
3. Press Enter
4. Create shortcut to `start_production.bat` in this folder

---

## 🔍 **Check if It's Running**

```powershell
# Check the server process
Get-Process python | Where-Object {$_.MainWindowTitle -like "*GhostDrop*"}

# Check port 5000
netstat -ano | findstr :5000

# Or just open browser
# http://localhost:5000
```

---

## 🛑 **To Stop the Server**

### **If running in terminal:**
Press `Ctrl + C`

### **If running as task:**
```powershell
# Find Python process using port 5000
netstat -ano | findstr :5000

# Kill it (replace <PID> with actual number)
taskkill /PID <PID> /F

# Or stop task in Task Scheduler
schtasks /end /tn "GhostDrop Server"
```

---

## 🔄 **Access from Other Devices**

### **On Your Network (LAN):**

1. **Find your IP address:**
   ```powershell
   ipconfig | findstr IPv4
   ```
   Look for something like: `192.168.1.100`

2. **Access from phone/laptop:**
   ```
   http://192.168.1.100:5000
   ```

### **From Internet (Advanced):**
- Use Render.com deployment (see DEPLOYMENT.md)
- Or setup port forwarding on your router (not recommended for security)

---

## 🛡️ **Production Checklist**

Before running permanently:

1. ✅ **Change SECRET_KEY** in `.env`:
   ```
   SECRET_KEY=paste-random-long-string-here-min-32-characters
   ```
   Generate one: https://randomkeygen.com/

2. ✅ **Set production mode** in `.env`:
   ```
   FLASK_ENV=production
   DEBUG=False
   ```

3. ✅ **Ensure MongoDB is running:**
   ```powershell
   net start MongoDB
   ```

4. ✅ **Test upload/download** before making it permanent

---

## 🎯 **Recommended: Use Production Server (Waitress)**

Instead of `run.py` (development), use `run_production.py` (production-ready):

```powershell
python run_production.py
```

**Why Waitress?**
- Production-ready WSGI server
- Better performance
- Handles multiple requests better
- More stable than Flask development server

---

## ☁️ **Alternative: Deploy to Cloud (Zero Maintenance)**

If you want it accessible from anywhere without keeping your PC on:

### **Render.com (Free):**
1. Push code to GitHub
2. Connect Render.com to GitHub
3. It auto-deploys with HTTPS
4. Get URL: `https://your-app.onrender.com`

See full guide: **DEPLOYMENT.md**

---

## 📋 **Quick Commands**

```powershell
# Start production server manually
python run_production.py

# Start MongoDB service
net start MongoDB

# Check if running
netstat -ano | findstr :5000

# View running tasks
schtasks /query /tn "GhostDrop Server"

# Run task manually
schtasks /run /tn "GhostDrop Server"

# Delete task
schtasks /delete /tn "GhostDrop Server"
```

---

## ✅ **Summary**

**Best solution for "run forever":**
1. Use **Task Scheduler** method above
2. Server starts automatically on Windows boot
3. Restarts automatically if it crashes
4. No need to keep terminal open
5. Runs in background

**Test it:**
```powershell
# Reboot your computer
# GhostDrop should start automatically
# Check: http://localhost:5000
```

---

**You're done! GhostDrop will now run forever until you stop it manually.** 🎉
