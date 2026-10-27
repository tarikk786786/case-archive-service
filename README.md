# Free 24/7 Cloud Streaming Archive Server (Render.com)

This lightweight service streams the **11.00 GB `Case_2026_Forensic_Archive.zip`** dynamically in real time without storing an 11 GB file on disk. It runs **24/7 in the cloud for free**, allowing anyone to download it at an enforced slow speed even when your computer is completely turned off.

---

## Key Benefits
- **Works 24/7 with PC Turned Off**: Hosted on Render's cloud infrastructure.
- **Zero Cloud Disk Usage (0 MB)**: Uses an on-the-fly streaming engine to generate the 11 GB ZIP64 file in real-time.
- **Enforced Slow Speed**: Downloads at a fixed rate (default **200 KB/s** or **100 KB/s**), making it take ~15–30 hours to download.
- **WhatsApp Compatible**: Provides a permanent HTTPS link you can send directly in WhatsApp messages.
- **RFC 7233 Resumable**: Mobile devices can pause, lose signal, and resume without losing progress.

---

## 2-Minute Deployment Guide to Render (100% Free)

### Step 1: Push this `render_app` folder to a new GitHub repository
1. Go to [github.com/new](https://github.com/new) and create a repository (e.g. `case-archive-service`).
2. Upload the 3 files in this folder:
   - `main.py`
   - `render.yaml`
   - `requirements.txt`

### Step 2: Connect to Render.com
1. Go to [dashboard.render.com](https://dashboard.render.com) and sign up/log in (free).
2. Click **New +** $\rightarrow$ **Web Service**.
3. Select **Build and deploy from a Git repository**.
4. Choose your new repository (`case-archive-service`).

### Step 3: Configure & Deploy
Render will automatically detect the settings:
- **Runtime**: `Python`
- **Build Command**: *(leave empty)*
- **Start Command**: `python main.py`
- **Instance Type**: `Free`
- **Environment Variables**:
  - `RATE_LIMIT_KBPS` = `200` *(change to `100` if you want it even slower)*

Click **Deploy Web Service**!

---

## Your Permanent 24/7 Links
Once deployed, Render gives you a live HTTPS link (e.g. `https://safe-case-archive-2026.onrender.com`):

- **Direct Download Link (Send on WhatsApp)**:
  ```text
  https://safe-case-archive-2026.onrender.com/Case_2026_Forensic_Archive.zip
  ```
- **Web Download Portal**:
  ```text
  https://safe-case-archive-2026.onrender.com/
  ```
- **Status Endpoint**:
  ```text
  https://safe-case-archive-2026.onrender.com/status
  ```
