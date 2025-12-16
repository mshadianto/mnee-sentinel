# ✅ MNEE Sentinel - Pre-Demo Checklist

## Complete this 30 minutes before your presentation

---

## 🔧 **Technical Setup** (15 minutes)

### **1. Environment Check**

- [ ] Python 3.11+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list` shows all packages)
- [ ] No error messages when running `python -c "import streamlit"`

```bash
# Quick test
source venv/bin/activate
python -c "
from utils.crypto_utils import MNEETokenManager
from utils.db_utils import GovernanceDB
from agents.auditor_agent import AuditorAgent
print('✅ All imports successful!')
"
```

---

### **2. API Keys Configuration**

- [ ] `.env` file exists
- [ ] Groq API key is ACTIVE (test at console.groq.com)
- [ ] Supabase URL is correct
- [ ] Supabase key is correct
- [ ] Test connection works

```bash
# Test API keys
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Groq:', 'OK' if os.getenv('GROQ_API_KEY') else 'MISSING')
print('Supabase:', 'OK' if os.getenv('SUPABASE_URL') else 'MISSING')
"
```

---

### **3. Database Setup**

- [ ] Supabase project is running
- [ ] `db_schema.sql` has been executed
- [ ] 10 budget categories exist
- [ ] 10 Indonesian vendors exist
- [ ] Sample audit logs exist (for Tab 3 demo)

**Verify in Supabase:**
```sql
-- Check budgets
SELECT COUNT(*) FROM budgets; 
-- Should return: 10

-- Check vendors
SELECT COUNT(*) FROM whitelisted_vendors;
-- Should return: 10

-- Check audit logs
SELECT COUNT(*) FROM audit_logs;
-- Should return: 3+ (sample data)
```

---

### **4. Application Launch**

- [ ] Dashboard starts without errors
- [ ] Opens at `http://localhost:8501`
- [ ] No error messages in terminal
- [ ] AI provider selector shows 3 options
- [ ] Treasury balance displays (even if 0)

```bash
# Start app
streamlit run app.py

# Check terminal for errors
# Should see: "You can now view your Streamlit app..."
```

---

## 🎨 **Visual Check** (5 minutes)

### **5. UI Verification**

- [ ] **Tab 1** (Submit Proposal) loads
  - [ ] PDF upload widget visible
  - [ ] Manual text area visible
  - [ ] Submit button works
  
- [ ] **Tab 2** (Budget Analytics) loads
  - [ ] Pie chart displays
  - [ ] Bar chart displays
  - [ ] Progress bars show
  
- [ ] **Tab 3** (Audit History) loads
  - [ ] Sample logs display
  - [ ] Can expand entries
  - [ ] Reasoning is visible
  
- [ ] **Tab 4** (Vendor Management) loads
  - [ ] 10 Indonesian vendors show
  - [ ] Table is formatted

---

### **6. Sidebar Check**

- [ ] AI Provider dropdown shows:
  - ⚡ Groq (Llama 3.1) - Fastest
  - 🎯 OpenAI (GPT-4) - Accurate
  - 🧠 Claude (Sonnet 4) - Best
  
- [ ] **Groq is selected** (for demo speed)
- [ ] Treasury balance shows
- [ ] Network info displays

---

## 🧪 **Test Run** (5 minutes)

### **7. Rejection Test**

**Input:**
```
Transfer 1000 MNEE to PT Cloud Treasury Tools (0xD4e5F60718293aBcD4E5F60718293aBcD4E5F607) for cloud services
```

**Expected:**
- [ ] ❌ Submits successfully
- [ ] 🔴 Big RED alert appears
- [ ] "TRANSACTION BLOCKED" is visible
- [ ] Risk level shows "HIGH"
- [ ] Detailed reasoning displays
- [ ] Numbers are clear (1000 vs 90)

**If this fails, STOP and debug!**

---

### **8. Approval Test**

**Input:**
```
Transfer 50 MNEE to PT Nusantara FX Services (0xA1b2C3D4e5F60718293aBcD4E5F60718293aBcD4) for FX hedging
```

**Expected:**
- [ ] ✅ Submits successfully
- [ ] 🟢 Big GREEN alert appears
- [ ] "APPROVED" is visible
- [ ] Risk level shows "LOW"
- [ ] All checkmarks show
- [ ] Execute button appears

**If this fails, STOP and debug!**

---

### **9. Audit Trail Test**

- [ ] Go to Tab 3
- [ ] Recent audit shows (rejection from step 7)
- [ ] Can expand entry
- [ ] Reasoning is detailed
- [ ] Risk badge shows (🔴 HIGH RISK)

---

## 📝 **Content Preparation** (3 minutes)

### **10. Test Proposals Ready**

- [ ] Open `TEST_PROPOSALS.md`
- [ ] Copy rejection examples to notepad
- [ ] Copy approval examples to notepad
- [ ] Have them ready to paste (don't type live!)

**Recommended order:**
1. Budget exceeded (rejection)
2. Vendor not whitelisted (rejection)
3. Valid FX transaction (approval)

---

### **11. Demo Script Ready**

- [ ] `DEMO_SCRIPT.md` is open
- [ ] Key talking points highlighted
- [ ] Timing marked (2 minutes total)
- [ ] Backup scenarios noted

---

## 🖥️ **Presentation Setup** (2 minutes)

### **12. Browser Configuration**

- [ ] Browser in **fullscreen mode** (F11)
- [ ] Zoom level at 100% or 110%
- [ ] Only MNEE Sentinel tab open (close others)
- [ ] Disable notifications (Do Not Disturb)
- [ ] Close email, Slack, etc.

---

### **13. Screen Recording** (Optional but Recommended)

- [ ] Screen recorder ready (OBS, QuickTime, etc.)
- [ ] Audio test done
- [ ] Backup recording prepared

---

## 🎯 **Final Checks** (1 minute)

### **14. Quick Functionality Test**

Run this sequence FAST (30 seconds):

1. **Submit rejection** → See RED alert ✓
2. **Submit approval** → See GREEN alert ✓
3. **Check Tab 3** → See audit log ✓
4. **Check Tab 2** → See charts ✓

**All working? You're ready!**

---

### **15. Backup Plan**

- [ ] Have screenshots of working demo
- [ ] Have video recording as backup
- [ ] Know how to restart app if crash
- [ ] Have `TEST_PROPOSALS.md` printed/open

```bash
# Quick restart if needed
Ctrl+C  # Stop app
streamlit run app.py  # Restart
```

---

## 🚨 **Common Issues & Quick Fixes**

### **Issue: "Module not found"**
```bash
pip install -r requirements.txt
```

### **Issue: "Supabase connection error"**
```bash
# Check .env
cat .env | grep SUPABASE_URL
# Verify URL is correct
```

### **Issue: "AI provider not responding"**
```bash
# Switch to different provider in sidebar
# Or check API key is valid
```

### **Issue: "Dashboard won't load"**
```bash
# Clear Streamlit cache
streamlit cache clear
streamlit run app.py
```

---

## 🎬 **5 Minutes Before Demo**

### **Mental Preparation:**

- [ ] Take deep breath
- [ ] Review key talking points
- [ ] Test microphone
- [ ] Test screen sharing (if remote)
- [ ] Smile! You got this! 😊

### **Quick Run-Through:**

- [ ] Start app
- [ ] Test one rejection
- [ ] Test one approval
- [ ] Close test tabs

---

## 🏆 **Confidence Checklist**

**Can you:**

- [ ] Navigate all 4 tabs smoothly?
- [ ] Explain what "rejection" protects?
- [ ] Show detailed reasoning in audit trail?
- [ ] Explain the risk levels?
- [ ] Demo in under 2 minutes?

**All yes? You're ready to WIN!**

---

## 📋 **Emergency Contact Info**

**If demo environment fails:**

- Have backup video ready
- Have screenshots ready
- Know how to restart app
- Stay calm and explain concept verbally

---

## ✅ **FINAL GO/NO-GO Decision**

**Check all boxes:**

- [ ] App launches without errors
- [ ] Rejection test shows RED alert
- [ ] Approval test shows GREEN alert
- [ ] Audit trail displays
- [ ] AI provider is Groq (fast!)
- [ ] Test proposals ready
- [ ] Demo script reviewed
- [ ] Confidence level: HIGH

**ALL CHECKED? → GO FOR DEMO! 🚀**

**Any unchecked? → Debug NOW!**

---

<div align="center">

## 🎯 **You're Ready to Win!**

**Technical: ✅**  
**Content: ✅**  
**Confidence: ✅**

### **Show them the BLOCKING power!**

### **Good luck!** 🏆

</div>

---

## 📞 **Last-Minute Help**

**5 minutes before demo and something's wrong?**

1. **Don't panic**
2. **Have backup video/screenshots**
3. **Restart app**: `Ctrl+C` then `streamlit run app.py`
4. **Switch to manual explanation** if needed
5. **Judges care about CONCEPT more than perfect execution**

**Breathe. You got this!** 💪
