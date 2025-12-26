# Quick Deployment Guide 🚀

Your exam scheduling application is ready to deploy! Here are the **3 easiest options**:

---

## Option 1: Streamlit Cloud (Recommended - FREE & Easiest)

**Perfect for:** Demo, testing, small-medium deployments  
**Time:** 10 minutes  
**Cost:** FREE

### Step-by-Step:

1. **Push to GitHub** (if not already done):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/exam-scheduling.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to: https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `exam-scheduling`
   - Main file: `app.py`
   - Click "Advanced settings" → "Secrets"
   - Add your database credentials:
     ```toml
     DB_HOST = "your-database-host"
     DB_PORT = "5432"
     DB_NAME = "exam_scheduling"
     DB_USER = "your-username"
     DB_PASSWORD = "your-password"
     ```
   - Click "Deploy"

3. **Your app will be live at**: `https://YOUR_USERNAME-exam-scheduling.streamlit.app`

### Database Options for Streamlit Cloud:

**Option A: Supabase (FREE - Recommended)**
- Go to: https://supabase.com
- Create new project
- Get connection details from Settings → Database
- Use these credentials in Streamlit secrets

**Option B: ElephantSQL (FREE)**
- Go to: https://www.elephantsql.com
- Create Tiny Turtle (FREE) instance
- Copy connection URL
- Use credentials in Streamlit secrets

---

## Option 2: Railway (Modern & Easy - $5 FREE credit)

**Perfect for:** Production-ready deployment with database included  
**Time:** 15 minutes  
**Cost:** $5 FREE monthly, then ~$10-20/month

### Step-by-Step:

1. **Push to GitHub** (if not already done)

2. **Deploy on Railway**:
   - Go to: https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect and deploy

3. **Add PostgreSQL Database**:
   - In your project, click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically set environment variables

4. **Initialize Database**:
   - Go to your service → "Settings" → "Deploy"
   - Add initialization command (optional):
     ```bash
     python scripts/init_database.py && python scripts/generate_data.py
     ```

5. **Your app will be live at**: Railway provides a URL automatically

---

## Option 3: Render (Easy - FREE tier available)

**Perfect for:** Simple deployment with database  
**Time:** 15 minutes  
**Cost:** FREE tier available

### Step-by-Step:

1. **Push to GitHub**

2. **Deploy on Render**:
   - Go to: https://render.com
   - Sign up with GitHub
   - Click "New" → "Web Service"
   - Connect your repository
   - Settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   
3. **Add PostgreSQL**:
   - Click "New" → "PostgreSQL"
   - Connect to your web service

4. **Set Environment Variables**:
   - Add database credentials from PostgreSQL instance

---

## My Recommendation for You

Based on your project (13,000+ students, 110 formations, 1,118 modules):

### For Quick Demo/Testing:
✅ **Streamlit Cloud + Supabase**
- FREE
- 5 minutes to deploy
- Perfect for showing to stakeholders

### For Production Use:
✅ **Railway**
- $5 FREE credit (enough for 1 month)
- Includes PostgreSQL
- Better performance
- Easy to scale

### For University Deployment:
✅ **Contact Your University IT Department**
- FREE (use university servers)
- On-premises (data privacy)
- Best for 13,000+ students
- See full guide in `DEPLOYMENT_GUIDE.md`

---

## Current Status of Your Application

✅ All files ready for deployment:
- `app.py` - Main application
- `requirements.txt` - Updated with all dependencies (including openpyxl)
- `Procfile` - For Heroku/Railway
- `railway.json` - For Railway
- `nixpacks.toml` - For Railway
- `runtime.txt` - Python version
- All source code committed to git

✅ Features working:
- EDT generation (1,118 exams in ~78 seconds)
- Planning by formation (NEW)
- Planning by department
- Conflict detection
- Statistics and analytics
- Excel/CSV export

✅ Database ready:
- 7 departments
- 110 formations
- 13,051 students
- 148 professors
- 1,118 modules
- 105,468 enrollments
- 126 rooms

---

## Next Steps (Choose One Path)

### Path A: Quick Demo (10 minutes)
```bash
# 1. Push to GitHub
git push origin main

# 2. Go to share.streamlit.io and deploy
# 3. Add database secrets
# 4. Done!
```

### Path B: Production Deployment (15 minutes)
```bash
# 1. Push to GitHub
git push origin main

# 2. Go to railway.app
# 3. Deploy from GitHub
# 4. Add PostgreSQL
# 5. Done!
```

### Path C: University Server (Contact IT)
```bash
# Send email to IT department with:
# - Link to repository
# - DEPLOYMENT_GUIDE.md
# - Server requirements (4GB RAM, PostgreSQL)
```

---

## Database Migration (If Needed)

If you need to export your current database to the hosted one:

```bash
# Export current database
pg_dump exam_scheduling > exam_scheduling_backup.sql

# Import to hosted database
psql -h YOUR_HOST -U YOUR_USER -d exam_scheduling < exam_scheduling_backup.sql
```

Or use the initialization scripts:
```bash
python scripts/init_database.py
python scripts/generate_data.py
```

---

## Support & Troubleshooting

### Common Issues:

**Issue: Database connection fails**
- Check credentials in secrets/environment variables
- Verify database host is accessible
- Check firewall/security group settings

**Issue: Application crashes on startup**
- Check logs for error messages
- Verify all dependencies in requirements.txt
- Ensure Python version matches (3.9+)

**Issue: Slow performance**
- Upgrade to paid tier for more resources
- Optimize database queries
- Consider university server for large scale

### Get Help:
- Full documentation: `DEPLOYMENT_GUIDE.md`
- Installation guide: `INSTALLATION.md`
- Test reports: `TEST_REPORT.md`

---

## Ready to Deploy?

**I recommend starting with Streamlit Cloud for a quick demo:**

1. Create GitHub repository (if not exists)
2. Push your code: `git push origin main`
3. Go to https://share.streamlit.io
4. Deploy in 3 clicks
5. Share the URL with stakeholders

**Then move to Railway for production when ready!**

---

Good luck with your deployment! 🎉
