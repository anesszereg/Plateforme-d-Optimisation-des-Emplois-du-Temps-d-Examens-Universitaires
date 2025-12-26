# Streamlit Cloud Deployment Fix 🔧

## Issue
Your deployment is failing with a DNS error. This is typically caused by:
1. Missing Python version specification
2. Missing system packages for PostgreSQL
3. Database connection not configured

## Solution

I've created the necessary files to fix this:

### Files Created:
1. **`.python-version`** - Specifies Python 3.11 (compatible with Streamlit Cloud)
2. **`packages.txt`** - System packages needed for PostgreSQL
3. **`secrets.toml.example`** - Template for database secrets

---

## Step-by-Step Fix

### 1. Commit and Push New Files

```bash
cd "/Users/mac/Desktop/DB PROJECT"

# Add new files
git add .python-version packages.txt secrets.toml.example STREAMLIT_DEPLOY_FIX.md

# Commit
git commit -m "Fix Streamlit Cloud deployment configuration"

# Push to GitHub
git push origin main
```

### 2. Configure Database on Streamlit Cloud

You need a hosted PostgreSQL database. Choose one:

#### Option A: Supabase (Recommended - FREE)

1. Go to: https://supabase.com
2. Create new project
3. Wait for database to initialize (~2 minutes)
4. Go to **Settings** → **Database**
5. Copy these values:
   - Host
   - Database name
   - User
   - Password
   - Port (usually 5432)

#### Option B: ElephantSQL (FREE - Limited)

1. Go to: https://www.elephantsql.com
2. Create **Tiny Turtle** (FREE) instance
3. Copy the connection details

#### Option C: Neon (FREE - Modern)

1. Go to: https://neon.tech
2. Create new project
3. Copy connection details

### 3. Add Secrets to Streamlit Cloud

1. Go to your Streamlit Cloud app dashboard
2. Click on your app
3. Click **"⋮"** (three dots) → **"Settings"**
4. Go to **"Secrets"** section
5. Add this configuration (replace with your actual values):

```toml
DB_HOST = "your-actual-host.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "your-actual-password"
```

6. Click **"Save"**

### 4. Initialize Database

Once your app is deployed, you need to initialize the database.

#### Method 1: Use Supabase SQL Editor

1. Go to Supabase dashboard
2. Click **SQL Editor**
3. Run these scripts in order:

```sql
-- Copy content from database/schema.sql
-- Then run it

-- Copy content from database/queries.sql
-- Then run it

-- Copy content from database/indexes.sql
-- Then run it
```

#### Method 2: Use Local Connection

```bash
# Export your database
pg_dump exam_scheduling > exam_backup.sql

# Import to hosted database (replace with your credentials)
psql -h your-host.supabase.co -U postgres -d postgres < exam_backup.sql
```

#### Method 3: Run Scripts via Streamlit Cloud Terminal (if available)

If Streamlit Cloud provides terminal access:
```bash
python scripts/init_database.py
python scripts/generate_data.py
```

### 5. Redeploy

After pushing changes and configuring secrets:

1. Go to Streamlit Cloud dashboard
2. Your app should auto-redeploy
3. If not, click **"Reboot app"**

---

## Troubleshooting

### Error: "This site can't be reached"

**Cause:** App is still deploying or crashed during startup

**Solution:**
1. Check Streamlit Cloud logs for errors
2. Verify database credentials in secrets
3. Ensure database is accessible from internet

### Error: "ModuleNotFoundError"

**Cause:** Missing dependency

**Solution:**
1. Check `requirements.txt` is complete
2. Redeploy the app

### Error: "Database connection failed"

**Cause:** Wrong credentials or database not accessible

**Solution:**
1. Verify secrets are correct
2. Check database allows connections from Streamlit Cloud IPs
3. For Supabase: Enable "Direct Connection" in settings

### Error: "No module named 'psycopg2'"

**Cause:** PostgreSQL library not installed

**Solution:**
- Already fixed with `packages.txt` file
- Redeploy after pushing changes

---

## Alternative: Use Railway Instead

If Streamlit Cloud continues to have issues, Railway is easier:

### Quick Railway Deployment:

1. Go to: https://railway.app
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Click **"Add PostgreSQL"** from the "New" menu
6. Railway automatically:
   - Detects your app
   - Sets up database
   - Configures environment variables
   - Deploys everything

**Done!** Railway provides a working URL immediately.

**Cost:** $5 FREE credit monthly (enough for testing)

---

## Recommended Path

Given the DNS error, I recommend:

### For Quick Demo:
✅ **Railway** - Easier, includes database, works immediately

### For Free Hosting:
✅ **Streamlit Cloud** - Follow steps above carefully

### For Production:
✅ **University Server** - Best for 13,000+ students

---

## Current Status

✅ Files created:
- `.python-version` - Python 3.11 specification
- `packages.txt` - PostgreSQL system dependencies
- `secrets.toml.example` - Database configuration template

⏳ Next steps:
1. Commit and push new files
2. Set up hosted database (Supabase/ElephantSQL/Neon)
3. Add secrets to Streamlit Cloud
4. Initialize database
5. Redeploy

---

## Need Help?

If you continue to have issues:

1. **Check Streamlit Cloud Logs:**
   - Go to your app dashboard
   - Click "Manage app"
   - View logs for specific errors

2. **Try Railway Instead:**
   - Simpler deployment
   - Includes database
   - Better error messages

3. **Contact Support:**
   - Streamlit Community: https://discuss.streamlit.io
   - Create GitHub issue with error logs

---

**Ready to fix?** Start by committing the new files and setting up your database! 🚀
