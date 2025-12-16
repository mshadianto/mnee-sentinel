#!/bin/bash

# ===================================
# MNEE Sentinel Quick Start Script
# ===================================

echo "🛡️  MNEE Sentinel - Quick Start Installer"
echo "=========================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

if ! python3 -c 'import sys; assert sys.version_info >= (3, 11)' 2>/dev/null; then
    echo "❌ ERROR: Python 3.11+ required"
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies (this may take a few minutes)..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ All dependencies installed"
echo ""

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "🔐 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your credentials:"
    echo "   - SUPABASE_URL"
    echo "   - SUPABASE_KEY"
    echo "   - GROQ_API_KEY (or OPENAI_API_KEY or ANTHROPIC_API_KEY)"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Display next steps
echo "=========================================="
echo "🎉 Installation Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Setup Supabase:"
echo "   → Create account at https://supabase.com"
echo "   → Create new project"
echo "   → Run db_schema.sql in SQL Editor"
echo "   → Copy URL and API key to .env"
echo ""
echo "2. Get AI API Key (choose one):"
echo "   → Groq (FREE): https://console.groq.com"
echo "   → OpenAI: https://platform.openai.com/api-keys"
echo "   → Anthropic: https://console.anthropic.com/account/keys"
echo ""
echo "3. Edit your .env file:"
echo "   nano .env"
echo ""
echo "4. Run the application:"
echo "   source venv/bin/activate  # If not already activated"
echo "   streamlit run app.py"
echo ""
echo "=========================================="
echo "Happy Hacking! 🚀"
echo "=========================================="
