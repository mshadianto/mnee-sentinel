# 🔒 MNEE Sentinel - Security Checklist

## ⚠️ CRITICAL: Pre-GitHub Upload Checklist

Before uploading to GitHub or submitting to hackathon judges, **MUST** complete this checklist!

---

## 🚨 **Priority 1: API Keys & Secrets**

### **Files to NEVER Commit:**

- [ ] ✅ `.env` file is in `.gitignore`
- [ ] ✅ `.env` file does NOT exist in Git history
- [ ] ✅ No API keys in any `.py` files
- [ ] ✅ No private keys in code
- [ ] ✅ No database passwords in code

### **Verification Commands:**

```bash
# Check if .env is tracked by Git
git ls-files | grep .env
# Should return NOTHING

# Check for API keys in code
grep -r "sk-" *.py
grep -r "gsk_" *.py
grep -r "sk-ant-" *.py
# Should return NOTHING

# Check for private keys
grep -r "PRIVATE_KEY" *.py
grep -r "0x[a-fA-F0-9]{64}" *.py
# Should return NOTHING (except in .env.example as placeholder)
```

---

## 🔐 **Priority 2: .gitignore Configuration**

### **Checklist:**

- [x] ✅ `.gitignore` file exists in root
- [x] ✅ `.env` is listed in `.gitignore`
- [x] ✅ `venv/` is listed in `.gitignore`
- [x] ✅ `__pycache__/` is listed in `.gitignore`
- [x] ✅ `*.key` is listed in `.gitignore`
- [x] ✅ `*.pem` is listed in `.gitignore`

### **Verify .gitignore:**

```bash
# Check .gitignore exists
cat .gitignore | grep .env
# Should show: .env

# Test if Git ignores .env
git check-ignore .env
# Should return: .env
```

---

## 📋 **Priority 3: .env.example Validation**

### **Checklist:**

- [x] ✅ `.env.example` exists
- [x] ✅ `.env.example` has NO real API keys
- [x] ✅ All sensitive values are placeholders
- [x] ✅ Clear instructions for obtaining keys

### **Safe .env.example Format:**

```bash
# GOOD (Placeholders only)
GROQ_API_KEY=gsk_your_groq_api_key_here
OPENAI_API_KEY=sk-your-openai-api-key-here
TREASURY_PRIVATE_KEY=0xYourPrivateKeyHere

# BAD (Real keys - NEVER DO THIS!)
GROQ_API_KEY=gsk_abc123realkey456  ❌
OPENAI_API_KEY=sk-proj-realkey789  ❌
```

---

## 🔍 **Priority 4: Git History Scan**

### **Check for Accidentally Committed Secrets:**

```bash
# Scan entire Git history for API keys
git log -p | grep -i "api_key"
git log -p | grep "sk-"
git log -p | grep "gsk_"

# If you find leaked keys:
# 1. IMMEDIATELY revoke them on provider website
# 2. Use git-filter-branch or BFG Repo Cleaner to remove from history
# 3. Generate new keys
# 4. Force push cleaned history
```

### **Emergency Cleanup:**

```bash
# If secrets were committed, use BFG Repo Cleaner
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Remove secrets from history
bfg --replace-text passwords.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

---

## 🛡️ **Priority 5: Code Review**

### **Manual Code Scan:**

- [ ] ✅ No hardcoded API keys in `config/settings.py`
- [ ] ✅ No hardcoded wallet addresses (except MNEE contract)
- [ ] ✅ No hardcoded database passwords
- [ ] ✅ All secrets loaded from `os.getenv()`

### **Safe Pattern:**

```python
# GOOD ✅
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# BAD ❌
GROQ_API_KEY = "gsk_abc123realkey"
```

---

## 📊 **Priority 6: Submission Package**

### **What to Include in GitHub:**

- [x] ✅ All `.py` files
- [x] ✅ `requirements.txt`
- [x] ✅ `db_schema.sql`
- [x] ✅ `.env.example` (placeholders only!)
- [x] ✅ `.gitignore`
- [x] ✅ `README.md` and documentation
- [x] ✅ `quick_start.sh`

### **What to EXCLUDE:**

- [ ] ❌ `.env` (NEVER include!)
- [ ] ❌ `venv/` folder
- [ ] ❌ `__pycache__/` folders
- [ ] ❌ Any files with real API keys
- [ ] ❌ PDF test files (unless needed for demo)

---

## 🚀 **Priority 7: Pre-Push Verification**

### **Final Checks Before `git push`:**

```bash
# 1. Status check
git status
# Ensure .env is NOT listed

# 2. Check what will be committed
git diff --cached

# 3. Verify .gitignore is working
git ls-files | grep .env
# Should return NOTHING

# 4. Test clone
cd ..
git clone <your-repo-url> test-clone
cd test-clone
ls -la
# Verify .env does NOT exist

# 5. Test installation
pip install -r requirements.txt
# Should work without errors
```

---

## 🎯 **Priority 8: Post-Push Validation**

### **After Pushing to GitHub:**

1. **Visit your GitHub repo in browser**
2. **Check file list** - `.env` should NOT be visible
3. **Check commit history** - No API keys in any commit
4. **Try cloning** - `git clone <url>` and verify no secrets
5. **Test README** - Installation instructions work

---

## 🚨 **If You Accidentally Committed Secrets**

### **Emergency Response Plan:**

```bash
# Step 1: IMMEDIATELY revoke the exposed keys
# - Groq: console.groq.com → Delete API key
# - OpenAI: platform.openai.com → Delete API key
# - Supabase: Project settings → Reset API keys

# Step 2: Remove from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Step 3: Add to .gitignore (if not already)
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"

# Step 4: Force push (WARNING: This rewrites history!)
git push origin --force --all

# Step 5: Generate NEW API keys
# Never reuse exposed keys!
```

---

## ✅ **Final Security Audit**

### **Pre-Submission Checklist:**

```bash
# Run this complete audit
echo "=== MNEE Sentinel Security Audit ==="
echo ""

echo "1. Checking .gitignore..."
if [ -f .gitignore ]; then
    echo "✅ .gitignore exists"
    if grep -q "^.env$" .gitignore; then
        echo "✅ .env is in .gitignore"
    else
        echo "❌ .env NOT in .gitignore!"
    fi
else
    echo "❌ .gitignore missing!"
fi

echo ""
echo "2. Checking for .env file..."
if [ -f .env ]; then
    echo "⚠️  .env exists locally (OK if in .gitignore)"
    git check-ignore .env && echo "✅ .env is ignored by Git" || echo "❌ .env is NOT ignored!"
else
    echo "✅ No .env file (use .env.example as template)"
fi

echo ""
echo "3. Scanning for hardcoded secrets..."
if grep -r "sk-" *.py 2>/dev/null | grep -v ".env.example"; then
    echo "❌ Found potential API keys in code!"
else
    echo "✅ No API keys found in code"
fi

echo ""
echo "4. Checking Git tracking..."
git ls-files | grep -E "\.env$|.*\.key$|.*\.pem$" && echo "❌ Secrets are tracked!" || echo "✅ No secrets tracked"

echo ""
echo "=== Audit Complete ==="
```

---

## 📞 **Support Resources**

### **If You Need Help:**

1. **GitHub Security Alerts**: Check repo → Security tab
2. **Remove Secrets**: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
3. **BFG Repo Cleaner**: https://rtyley.github.io/bfg-repo-cleaner/

---

## 🎓 **Best Practices for Future**

### **Always:**
- ✅ Use `.env` for all secrets
- ✅ Add `.env` to `.gitignore` BEFORE first commit
- ✅ Use `os.getenv()` to load secrets
- ✅ Provide `.env.example` with placeholders

### **Never:**
- ❌ Hardcode API keys in code
- ❌ Commit `.env` to Git
- ❌ Share real credentials in documentation
- ❌ Reuse exposed API keys

---

<div align="center">

## 🔒 **Security is NOT Optional!**

**One leaked API key = Instant disqualification**

**Review this checklist TWICE before submission!**

### ✅ **When in doubt, DON'T commit it!**

</div>

---

## 📋 **Quick Copy-Paste Checklist**

Before final submission:

```
[ ] .env is in .gitignore
[ ] .env is NOT in Git history
[ ] No API keys in .py files
[ ] .env.example has only placeholders
[ ] Tested git clone (no secrets appear)
[ ] All API keys are ACTIVE and VALID
[ ] README has clear setup instructions
[ ] Tested fresh installation
```

**All checked? You're ready to submit!** 🚀
