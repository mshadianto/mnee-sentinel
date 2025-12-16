# 🚀 MNEE Sentinel - Complete Installation Guide

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Python 3.11+** installed
- [ ] **Git** installed (to clone repository)
- [ ] **Code editor** (VS Code, PyCharm, etc.)
- [ ] **Supabase account** (free tier available)
- [ ] **AI API Key** (Groq recommended - free tier)

---

## 🎯 Step-by-Step Installation

### Step 1: Setup Project Files

**Option A: Using the provided files**
```bash
# Extract the mnee-sentinel folder
cd mnee-sentinel
```

**Option B: Clone from GitHub** (if uploaded)
```bash
git clone <your-github-repo>
cd mnee-sentinel
```

---

### Step 2: Python Environment Setup

```bash
# Check Python version (must be 3.11+)
python3 --version

# Run the quick start script (Linux/Mac)
chmod +x quick_start.sh
./quick_start.sh

# OR manually create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Expected Output:**
```
✅ Python version OK
✅ Virtual environment created
✅ All dependencies installed
```

---

### Step 3: Setup Supabase Database

#### 3.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click **"New Project"**
3. Fill in details:
   - **Name**: mnee-sentinel
   - **Database Password**: [Save this!]
   - **Region**: Choose closest to you
4. Click **"Create new project"** (wait ~2 minutes)

#### 3.2 Run Database Schema

1. In Supabase Dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Copy contents of `db_schema.sql`
4. Paste into editor
5. Click **"Run"**

**Expected Output:**
```
Success. No rows returned
```

#### 3.3 Verify Tables Created

1. Go to **Table Editor** tab
2. You should see 4 tables:
   - ✅ budgets (10 rows)
   - ✅ whitelisted_vendors (10 rows)
   - ✅ audit_logs (3 sample rows)
   - ✅ transaction_velocity (0 rows)

#### 3.4 Get API Credentials

1. Go to **Project Settings** → **API**
2. Copy these values:
   ```
   Project URL: https://xxxxx.supabase.co
   anon public key: eyJhb...
   ```

---

### Step 4: Get AI API Key (Choose ONE)

#### **Option A: Groq (RECOMMENDED - Free & Fast)**

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google/GitHub
3. Click **"API Keys"** in sidebar
4. Click **"Create API Key"**
5. Copy key (starts with `gsk_`)

**Free Tier**: 14,400 requests/day ✅

#### **Option B: OpenAI (Most Accurate)**

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up / Log in
3. Go to **API Keys**
4. Click **"Create new secret key"**
5. Copy key (starts with `sk-`)

**Pricing**: ~$0.01 per request

#### **Option C: Anthropic (Best Reasoning)**

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up
3. Go to **Account** → **API Keys**
4. Click **"Create Key"**
5. Copy key (starts with `sk-ant-`)

**Free Tier**: $5 credit

---

### Step 5: Configure Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit the file
nano .env  # or use any text editor
```

**Fill in these values:**
```bash
# ===================================
# REQUIRED: Supabase Configuration
# ===================================
SUPABASE_URL=https://xxxxx.supabase.co  # From Step 3.4
SUPABASE_KEY=eyJhbGciOi...              # From Step 3.4

# ===================================
# REQUIRED: AI Provider (Choose ONE)
# ===================================
GROQ_API_KEY=gsk_xxxxx                  # From Step 4A
# OR
OPENAI_API_KEY=sk-xxxxx                 # From Step 4B
# OR
ANTHROPIC_API_KEY=sk-ant-xxxxx          # From Step 4C

AI_PROVIDER=groq  # or "openai" or "anthropic"

# ===================================
# OPTIONAL: Blockchain (for live transactions)
# ===================================
ETHEREUM_RPC_URL=https://eth.llamarpc.com
TREASURY_ADDRESS=0xYourWalletAddress
TREASURY_PRIVATE_KEY=0xYourPrivateKey  # ⚠️ KEEP SECRET!
```

**Save and close** (Ctrl+X, then Y, then Enter in nano)

---

### Step 6: Test the Installation

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Test imports
python3 -c "
from utils.crypto_utils import MNEETokenManager
from utils.db_utils import GovernanceDB
from agents.auditor_agent import AuditorAgent
print('✅ All imports successful!')
"
```

**Expected Output:**
```
✅ All imports successful!
```

---

### Step 7: Launch the Dashboard

```bash
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**The browser should automatically open!** 🎉

---

## 🎮 First-Time Usage

### Test with Sample Proposal

1. **Go to Tab 1: "Submit Proposal"**

2. **Enter this text:**
   ```
   Transfer 50 MNEE to PT Nusantara FX Services (0xA1b2C3D4e5F60718293aBcD4E5F60718293aBcD4) for FX hedging
   ```

3. **Click "Submit for AI Audit"**

4. **Expected Result:**
   ```
   ✅ APPROVED
   AI Confidence: 95%
   Provider: GROQ
   
   Reasoning:
   ✓ Vendor whitelisted
   ✓ Within vendor limit: 50 ≤ 100 MNEE
   ✓ Budget available: 200 MNEE remaining in FX
   ✓ Velocity check passed
   ```

5. **Click "Execute Transaction"** (it's simulated by default)

6. **Go to Tab 3: "Audit History"** to see the log

---

## ⚙️ Configuration Options

### Change AI Provider

**In Sidebar:**
- Select different provider from dropdown
- Changes apply immediately

**Or in .env file:**
```bash
AI_PROVIDER=openai  # Switch to OpenAI
```

### Adjust Confidence Threshold

**Edit `config/settings.py`:**
```python
CONFIDENCE_THRESHOLD = 0.80  # Require 80% confidence
```

### Add Custom Vendor

**In Supabase SQL Editor:**
```sql
INSERT INTO whitelisted_vendors 
(vendor_name, wallet_address, category, max_transaction_limit)
VALUES 
('My Custom Vendor', '0x1234...', 'Software', 75.00);
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
# Solution: Activate virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Supabase credentials not configured"
```bash
# Solution: Check .env file
cat .env | grep SUPABASE
# Ensure URL and KEY are set
```

### Issue: "No valid API key for provider"
```bash
# Solution: Check .env file
cat .env | grep API_KEY
# Ensure at least one AI provider key is set
```

### Issue: "Failed to connect to Ethereum RPC"
```bash
# Solution: Use a different RPC
# Edit .env:
ETHEREUM_RPC_URL=https://cloudflare-eth.com
```

### Issue: Streamlit shows blank page
```bash
# Solution: Clear cache and restart
streamlit cache clear
streamlit run app.py
```

---

## 🔒 Security Best Practices

### ⚠️ NEVER Commit These to Git:

```bash
# Add to .gitignore
.env
venv/
__pycache__/
*.pyc
```

### ✅ Safe to Share:

```
.env.example
README.md
db_schema.sql
All *.py files
```

---

## 📊 Verifying Everything Works

### Checklist:

- [ ] **Dashboard loads** (http://localhost:8501)
- [ ] **Treasury balance shows** (even if 0)
- [ ] **AI provider selected** in sidebar
- [ ] **Budget table displays** in Tab 2
- [ ] **Sample proposal parses** successfully
- [ ] **Audit logs appear** in Tab 3
- [ ] **Vendors list shows** in Tab 4

---

## 🚀 Next Steps

### For Hackathon Demo:

1. **Record 2-minute demo video**
   - Show dashboard
   - Submit a proposal
   - Show approval reasoning
   - Highlight audit trail

2. **Deploy to Streamlit Cloud** (optional)
   ```bash
   # Push to GitHub
   git init
   git add .
   git commit -m "MNEE Sentinel - Initial commit"
   git push origin main
   
   # Then go to share.streamlit.io
   # Connect your repo
   # Add secrets (SUPABASE_URL, etc.)
   ```

3. **Prepare pitch deck**
   - Problem statement
   - Solution architecture
   - Live demo
   - Impact metrics

---

## 📞 Getting Help

### Common Resources:

- **Supabase Docs**: https://supabase.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **LangChain Docs**: https://python.langchain.com
- **Web3.py Docs**: https://web3py.readthedocs.io

### Error Logs:

```bash
# Check Streamlit logs
streamlit run app.py --logger.level=debug

# Check Python errors
python3 app.py
```

---

## ✅ Installation Complete!

You're now ready to use **MNEE Sentinel** for your hackathon submission!

**Happy Hacking!** 🎉

---

<div align="center">

### Questions?

Check **README.md** for more details  
See **PROJECT_SUMMARY.md** for architecture overview

**MNEE Sentinel** - Securing Treasuries with AI

</div>
