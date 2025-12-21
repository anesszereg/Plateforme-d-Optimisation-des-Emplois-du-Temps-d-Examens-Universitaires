#!/bin/bash

# Exam Scheduling Platform - Quick Deployment Script
# This script helps you prepare the application for deployment

set -e

echo "=================================="
echo "Exam Scheduling - Deployment Setup"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if git is initialized
if [ ! -d .git ]; then
    print_warning "Git not initialized. Initializing..."
    git init
    print_success "Git initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    print_warning "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Environment
.env
.env.local
.env.production

# Streamlit
.streamlit/secrets.toml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF
    print_success ".gitignore created"
fi

# Create Streamlit config directory
mkdir -p .streamlit

# Create config.toml for production
if [ ! -f .streamlit/config.toml ]; then
    print_warning "Creating Streamlit config..."
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
    print_success "Streamlit config created"
fi

# Create secrets template
if [ ! -f .streamlit/secrets.toml.example ]; then
    print_warning "Creating secrets template..."
    cat > .streamlit/secrets.toml.example << 'EOF'
# Database Configuration
DB_HOST = "your-database-host"
DB_PORT = "5432"
DB_NAME = "exam_scheduling"
DB_USER = "your-username"
DB_PASSWORD = "your-password"

# Optional: Authentication
[passwords]
admin = "your-secure-password"
EOF
    print_success "Secrets template created"
fi

# Create Procfile for Heroku
if [ ! -f Procfile ]; then
    print_warning "Creating Procfile for Heroku..."
    echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
    print_success "Procfile created"
fi

# Create runtime.txt for Heroku
if [ ! -f runtime.txt ]; then
    print_warning "Creating runtime.txt..."
    echo "python-3.9.18" > runtime.txt
    print_success "runtime.txt created"
fi

# Create railway.json
if [ ! -f railway.json ]; then
    print_warning "Creating Railway config..."
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
    print_success "Railway config created"
fi

# Create nixpacks.toml for Railway
if [ ! -f nixpacks.toml ]; then
    print_warning "Creating nixpacks config..."
    cat > nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["python39", "postgresql"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"
EOF
    print_success "nixpacks config created"
fi

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    print_error "requirements.txt not found!"
    exit 1
fi

echo ""
echo "=================================="
print_success "Deployment files prepared!"
echo "=================================="
echo ""

# Show deployment options
echo "Choose your deployment platform:"
echo ""
echo "1. Streamlit Cloud (Easiest - FREE)"
echo "   - Push to GitHub"
echo "   - Go to share.streamlit.io"
echo "   - Connect repository and deploy"
echo ""
echo "2. Railway (Modern - FREE tier)"
echo "   - Install: npm install -g @railway/cli"
echo "   - Run: railway login && railway init && railway up"
echo ""
echo "3. Heroku (Classic - FREE tier)"
echo "   - Install Heroku CLI"
echo "   - Run: heroku create && git push heroku main"
echo ""
echo "4. DigitalOcean/AWS (Production)"
echo "   - See DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
echo "5. University Server (Recommended)"
echo "   - Contact your IT department"
echo "   - Provide DEPLOYMENT_GUIDE.md"
echo ""

# Ask if user wants to commit changes
read -p "Do you want to commit these changes to git? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .
    git commit -m "Add deployment configuration files"
    print_success "Changes committed to git"
    echo ""
    echo "Next steps:"
    echo "1. Create a GitHub repository"
    echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/exam-scheduling.git"
    echo "3. Run: git push -u origin main"
    echo "4. Deploy to your chosen platform"
fi

echo ""
print_success "Setup complete! See DEPLOYMENT_GUIDE.md for detailed instructions."
echo ""
