# GhostDrop Windows Service Setup Guide

## 🚀 Option 1: Run as Windows Startup Task (Easiest)

### Step 1: Create Startup Shortcut

1. **Open Startup folder:**
   ```
   Press Win+R
   Type: shell:startup
   Press Enter
   ```

2. **Create shortcut:**
   - Right-click → New → Shortcut
   - Location: `C:\Users\n2005\file sharingwebapp\start_ghostdrop.bat`
   - Name: `GhostDrop`
   - Click Finish

3. **Done!** GhostDrop will start automatically when Windows boots.

---

## 🔧 Option 2: Use Task Scheduler (Recommended)

### Create Scheduled Task

1. **Open Task Scheduler:**
   ```
   Press Win+R
   Type: taskschd.msc
   Press Enter
   ```

2. **Create Basic Task:**
   - Click "Create Task..." (right panel)
   - **General Tab:**
     - Name: `GhostDrop Server`
     - Description: `File sharing web app`
     - ☑ Run whether user is logged on or not
     - ☑ Run with highest privileges
     - Configure for: Windows 10/11

3. **Triggers Tab:**
   - New → Begin the task: `At startup`
   - Delay: 30 seconds (optional)
   - OK

4. **Actions Tab:**
   - New → Action: `Start a program`
   - Program: `C:\Users\n2005\file sharingwebapp\.venv\Scripts\python.exe`
   - Arguments: `run.py`
   - Start in: `C:\Users\n2005\file sharingwebapp`
   - OK

5. **Conditions Tab:**
   - ☐ Uncheck "Start only if on AC power" (for laptops)

6. **Settings Tab:**
   - ☑ Allow task to run on demand
   - ☑ If task fails, restart every: 1 minute
   - Attempt to restart: 3 times

7. **Click OK** and enter your Windows password

### Manage Task
```powershell
# Start
schtasks /run /tn "GhostDrop Server"

# Stop
taskkill /F /IM python.exe

# Check status
schtasks /query /tn "GhostDrop Server"
```

---

## 🛠️ Option 3: Windows Service with NSSM (Most Professional)

### Install NSSM (Non-Sucking Service Manager)

1. **Download NSSM:**
   ```
   https://nssm.cc/download
   ```
   Extract to: `C:\nssm`

2. **Install Service:**
   ```powershell
   # Open PowerShell as Administrator
   cd C:\nssm\win64
   
   .\nssm.exe install GhostDrop "C:\Users\n2005\file sharingwebapp\.venv\Scripts\python.exe" "run.py"
   
   .\nssm.exe set GhostDrop AppDirectory "C:\Users\n2005\file sharingwebapp"
   .\nssm.exe set GhostDrop DisplayName "GhostDrop File Sharing"
   .\nssm.exe set GhostDrop Description "Privacy-first temporary file sharing"
   .\nssm.exe set GhostDrop Start SERVICE_AUTO_START
   
   # Set environment variables
   .\nssm.exe set GhostDrop AppEnvironmentExtra FLASK_ENV=production
   
   # Start service
   .\nssm.exe start GhostDrop
   ```

3. **Manage Service:**
   ```powershell
   # Start
   net start GhostDrop
   
   # Stop
   net stop GhostDrop
   
   # Restart
   net stop GhostDrop && net start GhostDrop
   
   # Uninstall
   C:\nssm\win64\nssm.exe remove GhostDrop confirm
   ```

4. **Check Logs:**
   - Event Viewer → Windows Logs → Application
   - Look for "GhostDrop" events

---

## ☁️ Option 4: Deploy to Cloud (No Local Server Needed)

### Deploy to Render.com (Free Tier)

1. **Sign up:** https://render.com

2. **Connect GitHub:**
   - Create GitHub repo
   - Push your code:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin <your-repo-url>
     git push -u origin main
     ```

3. **Create Web Service:**
   - Dashboard → New → Web Service
   - Connect GitHub repo
   - Settings:
     - Name: `ghostdrop`
     - Environment: `Docker`
     - Plan: `Free`

4. **Add MongoDB:**
   - Create MongoDB Atlas account (free)
   - Get connection string
   - Add to Render Environment Variables:
     ```
     MONGODB_URI=mongodb+srv://...
     SECRET_KEY=<random-string>
     FLASK_ENV=production
     ```

5. **Deploy!** 
   - Render auto-deploys
   - Get URL: `https://ghostdrop.onrender.com`

### Deploy to Railway.app

1. **Install Railway CLI:**
   ```powershell
   npm install -g @railway/cli
   ```

2. **Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Add MongoDB plugin:**
   ```bash
   railway add mongodb
   ```

4. **Done!** Railway gives you a URL.

---

## 🔍 Check if Running

### Windows
```powershell
# Check if process is running
Get-Process python | Where-Object {$_.MainWindowTitle -like "*GhostDrop*"}

# Check port
netstat -ano | findstr :5000
```

### Test
Open browser: http://localhost:5000

---

## 🔄 Auto-Restart on Crash

### Using Forever (Node.js tool)
```bash
npm install -g forever
forever start -c python run.py
```

### Using PM2
```bash
npm install -g pm2
pm2 start run.py --interpreter python --name ghostdrop
pm2 startup windows
pm2 save
```

---

## 📊 Monitor Running Service

### Create monitoring script: `monitor.bat`
```batch
@echo off
:loop
timeout /t 60 /nobreak >nul
netstat -ano | findstr :5000 >nul
if errorlevel 1 (
    echo GhostDrop not running! Restarting...
    start "" "C:\Users\n2005\file sharingwebapp\start_ghostdrop.bat"
)
goto loop
```

---

## 🛡️ Security for Production

1. **Change SECRET_KEY in .env:**
   ```
   SECRET_KEY=<generate-long-random-string>
   ```

2. **Set production mode:**
   ```
   FLASK_ENV=production
   DEBUG=False
   ```

3. **Restrict to localhost only:**
   In `config.py`:
   ```python
   HOST = '127.0.0.1'  # Only local access
   ```

4. **Or allow LAN access:**
   ```python
   HOST = '0.0.0.0'  # LAN access (192.168.x.x)
   ```

---

## 🎯 Recommended Setup

**For Personal Use (Local Network):**
1. Use **Task Scheduler** method
2. Set to start at Windows startup
3. Configure auto-restart on failure
4. Access at: http://localhost:5000

**For Production (Internet Access):**
1. Deploy to **Render.com** (free, easy)
2. Use MongoDB Atlas (free tier)
3. Get HTTPS automatically
4. Zero maintenance

---

## 🆘 Troubleshooting

**Port already in use:**
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000
# Kill that process
taskkill /PID <process_id> /F
```

**MongoDB not connecting:**
```powershell
# Check MongoDB service
net start MongoDB
```

**Permission denied:**
```powershell
# Run PowerShell as Administrator
```

---

## 📝 Quick Commands Cheat Sheet

```powershell
# Start in background
.\start_ghostdrop.bat

# Start production server (Waitress)
.\start_production.bat

# Stop
.\stop_ghostdrop.bat

# Check if running
netstat -ano | findstr :5000

# View logs (if running in terminal)
Get-Content error.log -Tail 50 -Wait
```

---

**Choose Option 2 (Task Scheduler) for the simplest "set and forget" solution on Windows!**
