# Deployment Guide - Exam Scheduling Platform

## Yes, You Can Host It! 🚀

This guide covers multiple hosting options for your exam scheduling platform, from free to production-grade solutions.

---

## Table of Contents
1. [Quick Hosting Options](#quick-hosting-options)
2. [Option 1: Streamlit Cloud (Easiest - FREE)](#option-1-streamlit-cloud)
3. [Option 2: Heroku (Easy - FREE/PAID)](#option-2-heroku)
4. [Option 3: Railway (Modern - FREE/PAID)](#option-3-railway)
5. [Option 4: AWS/DigitalOcean (Production)](#option-4-production-hosting)
6. [Option 5: University Server (Recommended)](#option-5-university-server)
7. [Database Hosting](#database-hosting)
8. [Security Considerations](#security-considerations)

---

## Quick Hosting Options

| Platform | Cost | Difficulty | Best For |
|----------|------|------------|----------|
| **Streamlit Cloud** | FREE | ⭐ Easy | Demo, Testing |
| **Railway** | FREE tier | ⭐⭐ Medium | Small-Medium scale |
| **Heroku** | FREE tier | ⭐⭐ Medium | Small-Medium scale |
| **DigitalOcean** | $12/month | ⭐⭐⭐ Advanced | Production |
| **AWS** | Variable | ⭐⭐⭐⭐ Expert | Enterprise |
| **University Server** | FREE | ⭐⭐⭐ Medium | Best for universities |

---

## Option 1: Streamlit Cloud (Easiest - FREE)

**Best for:** Quick demos, testing, small deployments

### Pros
- ✅ Completely FREE
- ✅ Easiest to deploy (3 clicks)
- ✅ Automatic updates from GitHub
- ✅ Built-in SSL/HTTPS
- ✅ No server management

### Cons
- ❌ Limited resources (1GB RAM)
- ❌ Database must be hosted separately
- ❌ Public by default (can add authentication)
- ❌ Not suitable for 13,000+ students

### Step-by-Step Deployment

#### 1. Prepare Your Repository

```bash
cd "/Users/mac/Desktop/DB PROJECT"

# Create .streamlit/config.toml for production settings
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
EOF

# Create secrets template
cat > .streamlit/secrets.toml.example << 'EOF'
# Database Configuration
DB_HOST = "your-database-host.com"
DB_PORT = "5432"
DB_NAME = "exam_scheduling"
DB_USER = "your-username"
DB_PASSWORD = "your-password"
EOF

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for deployment"
```

#### 2. Push to GitHub

```bash
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/exam-scheduling.git
git branch -M main
git push -u origin main
```

#### 3. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Add secrets (database credentials) in Advanced settings
7. Click "Deploy"

**Your app will be live at:** `https://YOUR_USERNAME-exam-scheduling.streamlit.app`

---

## Option 2: Heroku (Easy - FREE/PAID)

**Best for:** Small to medium deployments with database included

### Pros
- ✅ FREE tier available (with limitations)
- ✅ Includes PostgreSQL database (FREE tier: 10k rows)
- ✅ Easy deployment
- ✅ Automatic SSL
- ✅ Add-ons ecosystem

### Cons
- ❌ FREE tier sleeps after 30 min inactivity
- ❌ Limited database on FREE tier
- ❌ Paid plans start at $7/month

### Step-by-Step Deployment

#### 1. Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Create Heroku Configuration Files

```bash
cd "/Users/mac/Desktop/DB PROJECT"

# Create Procfile
cat > Procfile << 'EOF'
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
EOF

# Create runtime.txt
cat > runtime.txt << 'EOF'
python-3.9.18
EOF

# Update requirements.txt for Heroku
cat >> requirements.txt << 'EOF'
gunicorn==21.2.0
EOF
```

#### 3. Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create new app
heroku create exam-scheduling-app

# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set STREAMLIT_SERVER_HEADLESS=true
heroku config:set STREAMLIT_SERVER_PORT=8501

# Deploy
git add .
git commit -m "Heroku deployment configuration"
git push heroku main

# Initialize database
heroku run python scripts/init_database.py
heroku run python scripts/generate_data.py

# Open app
heroku open
```

**Your app will be at:** `https://exam-scheduling-app.herokuapp.com`

---

## Option 3: Railway (Modern - FREE/PAID)

**Best for:** Modern deployment with excellent developer experience

### Pros
- ✅ $5 FREE credit monthly
- ✅ PostgreSQL included
- ✅ Modern UI and workflow
- ✅ Automatic deployments
- ✅ Better performance than Heroku FREE

### Cons
- ❌ Requires credit card for FREE tier
- ❌ Paid after FREE credit ($0.000231/GB-hour)

### Step-by-Step Deployment

#### 1. Prepare Railway Configuration

```bash
cd "/Users/mac/Desktop/DB PROJECT"

# Create railway.json
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# Create nixpacks.toml
cat > nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["python39", "postgresql"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"
EOF
```

#### 2. Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Add PostgreSQL database from "New" menu
7. Set environment variables:
   - `DB_HOST`: Use Railway's internal URL
   - `DB_PORT`: 5432
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`: From Railway PostgreSQL
8. Deploy automatically starts

**Your app will be at:** `https://exam-scheduling-production.up.railway.app`

---

## Option 4: Production Hosting (AWS/DigitalOcean)

**Best for:** Production deployments, full control, 13,000+ users

### Option 4A: DigitalOcean (Recommended for Production)

**Cost:** ~$12-24/month

#### Setup Steps

```bash
# 1. Create DigitalOcean Droplet
# - Ubuntu 22.04 LTS
# - 2GB RAM / 1 vCPU ($12/month)
# - Add SSH key

# 2. SSH into server
ssh root@your-droplet-ip

# 3. Install dependencies
apt update && apt upgrade -y
apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx

# 4. Setup PostgreSQL
sudo -u postgres createuser --interactive --pwprompt
sudo -u postgres createdb exam_scheduling

# 5. Clone your repository
cd /var/www
git clone https://github.com/YOUR_USERNAME/exam-scheduling.git
cd exam-scheduling

# 6. Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 7. Configure environment
cp .env.example .env
nano .env  # Edit with your database credentials

# 8. Initialize database
python scripts/init_database.py
python scripts/generate_data.py

# 9. Setup systemd service
cat > /etc/systemd/system/exam-scheduling.service << 'EOF'
[Unit]
Description=Exam Scheduling Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/exam-scheduling
Environment="PATH=/var/www/exam-scheduling/venv/bin"
ExecStart=/var/www/exam-scheduling/venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 10. Setup Nginx reverse proxy
cat > /etc/nginx/sites-available/exam-scheduling << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/exam-scheduling /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 11. Start the application
systemctl enable exam-scheduling
systemctl start exam-scheduling

# 12. Setup SSL with Let's Encrypt
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

**Your app will be at:** `https://your-domain.com`

---

## Option 5: University Server (Recommended)

**Best for:** University deployments with IT support

### Why This is Best for Universities

- ✅ FREE (university infrastructure)
- ✅ On-premises data (privacy/compliance)
- ✅ IT support available
- ✅ Existing authentication (LDAP/SSO)
- ✅ Unlimited resources
- ✅ No external dependencies

### Requirements

1. **Server Specifications:**
   - OS: Ubuntu 20.04+ or CentOS 8+
   - RAM: 4GB minimum (8GB recommended)
   - CPU: 2 cores minimum
   - Storage: 20GB minimum
   - PostgreSQL 12+

2. **Network:**
   - Internal network access
   - Optional: External access via VPN
   - Port 80/443 for web access

3. **Contact Your IT Department:**
   ```
   Subject: Request for Application Server - Exam Scheduling System
   
   Dear IT Team,
   
   I would like to deploy an exam scheduling optimization platform
   for our university. The system requires:
   
   - Ubuntu server with 4GB RAM, 2 CPU cores
   - PostgreSQL database
   - Python 3.9+ environment
   - Web server (Nginx/Apache)
   - SSL certificate for HTTPS
   
   The application is a Streamlit-based web platform that will help
   optimize exam scheduling for 13,000+ students across 7 departments.
   
   Repository: [Your GitHub URL]
   Documentation: See DEPLOYMENT_GUIDE.md
   
   Please let me know the next steps.
   
   Best regards,
   [Your Name]
   ```

### Deployment on University Server

Follow the same steps as **Option 4A (DigitalOcean)** but coordinate with IT for:
- Server provisioning
- Database setup
- SSL certificate
- Domain name (e.g., `exams.university.edu`)
- Backup configuration
- Authentication integration (LDAP/SSO)

---

## Database Hosting

If you need to host the database separately:

### Free Database Hosting

1. **ElephantSQL** (FREE tier: 20MB)
   - [elephantsql.com](https://www.elephantsql.com)
   - Good for testing only

2. **Supabase** (FREE tier: 500MB)
   - [supabase.com](https://supabase.com)
   - Better for small deployments

3. **Railway PostgreSQL** (FREE $5 credit)
   - Included with Railway deployment

### Paid Database Hosting

1. **AWS RDS PostgreSQL** ($15-50/month)
   - Production-grade
   - Automatic backups
   - Scalable

2. **DigitalOcean Managed PostgreSQL** ($15/month)
   - Easy to use
   - Good performance

3. **Heroku PostgreSQL** ($9-50/month)
   - Integrated with Heroku apps

---

## Security Considerations

### Essential Security Measures

1. **Environment Variables**
   ```bash
   # Never commit credentials to git
   echo ".env" >> .gitignore
   echo ".streamlit/secrets.toml" >> .gitignore
   ```

2. **Database Security**
   - Use strong passwords
   - Restrict database access by IP
   - Enable SSL for database connections
   - Regular backups

3. **Application Security**
   - Enable HTTPS (SSL certificate)
   - Add authentication (Streamlit supports basic auth)
   - Rate limiting
   - Input validation

4. **Add Authentication to Streamlit**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   [passwords]
   admin = "your-secure-password"
   ```
   
   Add to `app.py`:
   ```python
   import streamlit as st
   
   def check_password():
       def password_entered():
           if st.session_state["password"] == st.secrets["passwords"]["admin"]:
               st.session_state["password_correct"] = True
               del st.session_state["password"]
           else:
               st.session_state["password_correct"] = False
       
       if "password_correct" not in st.session_state:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           return False
       elif not st.session_state["password_correct"]:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           st.error("😕 Password incorrect")
           return False
       else:
           return True
   
   if not check_password():
       st.stop()
   ```

---

## Recommended Deployment Path

### For Testing/Demo
1. **Streamlit Cloud** - Quick and free
2. Host database on **Supabase** (FREE)

### For Small University (< 5,000 students)
1. **Railway** - Modern and easy
2. Integrated PostgreSQL
3. Cost: ~$10-20/month

### For Medium University (5,000-15,000 students)
1. **DigitalOcean Droplet** - $24/month (4GB RAM)
2. **DigitalOcean Managed PostgreSQL** - $15/month
3. Total: ~$40/month

### For Large University (15,000+ students)
1. **University Server** - FREE, best option
2. On-premises database
3. IT support included

---

## Quick Start Commands

### Deploy to Streamlit Cloud (Fastest)
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/exam-scheduling.git
git push -u origin main

# 2. Go to share.streamlit.io and deploy
# 3. Add database secrets
# 4. Done!
```

### Deploy to Railway (Recommended)
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up

# 3. Add PostgreSQL
railway add postgresql

# 4. Set environment variables
railway variables set DB_HOST=...
```

---

## Monitoring & Maintenance

### Essential Monitoring

1. **Application Health**
   - Use UptimeRobot (FREE) for uptime monitoring
   - Set up alerts for downtime

2. **Database Backups**
   ```bash
   # Automated daily backup
   0 2 * * * pg_dump exam_scheduling > /backups/exam_$(date +\%Y\%m\%d).sql
   ```

3. **Log Monitoring**
   ```bash
   # View Streamlit logs
   tail -f /var/log/exam-scheduling/app.log
   ```

---

## Cost Summary

| Deployment | Monthly Cost | Best For |
|------------|--------------|----------|
| Streamlit Cloud + Supabase | **$0** | Testing |
| Railway | **$10-20** | Small scale |
| Heroku | **$16** | Small-medium |
| DigitalOcean | **$40** | Medium scale |
| University Server | **$0** | **Best option** |

---

## Support & Help

### If You Need Help

1. **Documentation**: Check `README.md` and `INSTALLATION.md`
2. **Issues**: Create GitHub issue
3. **University IT**: Contact for server access
4. **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)

### Next Steps

1. Choose your hosting platform
2. Follow the step-by-step guide above
3. Test with small dataset first
4. Deploy to production
5. Monitor and maintain

---

**Ready to deploy? Start with Streamlit Cloud for a quick demo, then move to Railway or your university server for production!** 🚀
