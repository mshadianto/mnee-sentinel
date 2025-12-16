# 🎬 MNEE Sentinel - Hackathon Demo Script

## 🎯 **2-Minute Winning Demo** (Show REJECTION First!)

---

## 🎭 **Act 1: Introduction** (15 seconds)

**Narasi:**
> "Hi judges! Saya presentasi **MNEE Sentinel** - AI yang melindungi treasury DAO dari kesalahan fatal."

**Action:**
- Tunjukkan dashboard
- Sidebar: pilih "Groq (Llama 3.1) - Fastest"

---

## 🔴 **Act 2: BLOCKING - Show AI Protection** (45 seconds)

### **Scenario 1: Budget Exceeded (CRITICAL)**

**Narasi:**
> "Pertama, saya tunjukkan bagaimana AI **MELINDUNGI** uang Anda."

**Input Proposal:**
```
Transfer 1000 MNEE to PT Cloud Treasury Tools 
(0xD4e5F60718293aBcD4E5F6071829AbcD4) for cloud services
```

**Action:**
- Paste di proposal text area
- Click "Submit for AI Audit"
- Wait 2-3 seconds

**Expected Result:**
```
🚫 TRANSACTION BLOCKED

AI Confidence: 95% | Provider: GROQ
RISK LEVEL: HIGH

❌ Insufficient Budget in Software Category

Required: 1000 MNEE
Remaining: 90 MNEE
Total Budget: 90 MNEE
Shortfall: 910 MNEE
```

**Narasi:**
> "**LIHAT!** Pop-up MERAH besar. AI menolak karena budget cuma 90 MNEE, 
> tapi diminta 1000 MNEE. Ini melindungi dari bankruptcy. 
> **Risk Level: HIGH** - sistem mendeteksi bahaya."

**Pause for effect** (5 seconds)

---

### **Scenario 2: Vendor Not Whitelisted (CRITICAL)**

**Narasi:**
> "Sekarang, coba vendor yang TIDAK terdaftar."

**Input Proposal:**
```
Transfer 50 MNEE to PT Hantu Consulting 
(0x0000000000000000000000000000000000000000) for advisory
```

**Action:**
- Clear previous proposal
- Paste new proposal
- Click "Submit for AI Audit"

**Expected Result:**
```
🚫 TRANSACTION BLOCKED

RISK LEVEL: CRITICAL

❌ Vendor Not Whitelisted

Vendor: PT Hantu Consulting
Address: 0x0000000000000000000000000000000000000000

This vendor is not authorized to receive treasury funds.
```

**Narasi:**
> "**BLOCKED!** Vendor 'PT Hantu' tidak ada di whitelist database. 
> AI mencegah fraud. **Risk: CRITICAL**."

---

## 🟢 **Act 3: APPROVAL - Show Normal Flow** (30 seconds)

**Narasi:**
> "Sekarang, transaksi yang VALID."

**Input Proposal:**
```
Transfer 50 MNEE to PT Nusantara FX Services 
(0xA1b2C3D4e5F60718293aBcD4E5F6071829Ab) for FX hedging
```

**Action:**
- Clear previous
- Paste valid proposal
- Click "Submit for AI Audit"

**Expected Result:**
```
✅ APPROVED

AI Confidence: 95% | Provider: GROQ
RISK LEVEL: LOW

✅ ALL COMPLIANCE CHECKS PASSED

✓ Vendor whitelisted: PT Nusantara FX Services
✓ Within vendor limit: 50 MNEE ≤ 100 MNEE
✓ Budget available: 200 MNEE remaining in FX
✓ Velocity check passed
```

**Narasi:**
> "**HIJAU!** Semua check PASSED. Vendor valid, budget cukup, limit OK. 
> AI approve dalam 2 detik."

**Action:**
- Click "Execute Transaction"
- Show success message

---

## 📊 **Act 4: Audit Trail** (20 seconds)

**Narasi:**
> "Yang penting: **FULL AUDIT TRAIL**."

**Action:**
- Go to Tab 3: Audit History
- Expand first rejected entry

**Show:**
```
🚫 PT Cloud Treasury Tools - 1000 MNEE
🔴 HIGH RISK

Detailed Reasoning:
❌ Insufficient Budget in Software Category
Required: 1000 MNEE
Remaining: 90 MNEE
Shortfall: 910 MNEE

AI Confidence: 95% (GROQ)
Timestamp: 2024-12-15 14:30:00
```

**Narasi:**
> "Setiap keputusan dicatat dengan REASONING lengkap. 
> Bisa di-export untuk regulator. Ini bukan AI wrapper biasa - 
> ini **AI Agent** yang benar-benar cerdas."

---

## 🎯 **Act 5: Closing** (10 seconds)

**Narasi:**
> "MNEE Sentinel: 
> - ✅ Solves real DAO problem
> - ✅ Uses MNEE token  
> - ✅ AI-powered governance
> - ✅ Perfect audit trail
> 
> **Thank you!**"

---

## 📋 **Props Checklist**

Before demo:
- [ ] Dashboard running on `localhost:8501`
- [ ] Groq API key configured (for speed)
- [ ] Database seeded with Indonesian vendors
- [ ] Budget limits set (Software: 90 MNEE)
- [ ] Browser in fullscreen mode
- [ ] Test proposals saved in notepad

---

## 🎨 **Visual Impact Points**

### **REJECTION Display:**
- 🔴 Big RED box with pulse animation
- **"TRANSACTION BLOCKED"** in huge text
- Risk level badge: "CRITICAL" or "HIGH"
- Detailed reasoning with numbers

### **APPROVAL Display:**
- 🟢 Big GREEN box
- **"APPROVED"** in huge text
- Risk level badge: "LOW"
- All checks with ✓ marks

### **Contrast:**
- Red vs Green is VERY visible
- Risk badges (🔴🟡🟢) add clarity
- Icons (🚫 vs ✅) are universal

---

## 🎤 **Key Talking Points**

### **Why Show Rejection First?**

1. **Proves governance works** - Not just approval theater
2. **Shows AI intelligence** - Can actually block bad transactions
3. **Demonstrates risk detection** - HIGH/CRITICAL badges
4. **Builds trust** - "This protects your money"

### **Why This Wins:**

1. **Real protection** - Not just logging, actual blocking
2. **Detailed reasoning** - Shows why, not just what
3. **Risk levels** - Security-conscious design
4. **Audit trail** - Regulator-ready compliance

---

## 🚨 **Common Demo Mistakes to Avoid**

❌ **DON'T:**
- Start with successful transaction (boring!)
- Skip showing the RED rejection screen
- Mumble through the reasoning
- Forget to show audit trail

✅ **DO:**
- Start with dramatic REJECTION
- Emphasize the BIG RED alert
- Read out the reasoning clearly
- Show complete audit history

---

## 📊 **Backup Scenarios** (If Time Permits)

### **Scenario 3: Velocity Check**
```
Transfer 50 MNEE to PT Nusantara (same vendor, 11th time today)

Result: 🚫 BLOCKED
Reason: Exceeded max transactions (10/day)
Risk: HIGH
```

### **Scenario 4: PDF Upload**
```
Upload invoice PDF
→ AI extracts data
→ Auto-generates proposal
→ Submits for validation
```

---

## 🎬 **Rehearsal Checklist**

Practice until you can:
- [ ] Complete demo in under 2 minutes
- [ ] Navigate without hesitation
- [ ] Explain each rejection clearly
- [ ] Show confidence in the product

---

## 🏆 **Judge Impact Strategy**

### **First 30 seconds:**
- Show BLOCKING feature (unique!)
- Create "wow" moment with RED alert

### **Next 30 seconds:**
- Show it also approves (balanced)
- Emphasize speed (2 seconds)

### **Last 60 seconds:**
- Audit trail (compliance angle)
- Technical depth (AI reasoning)
- Business value (protects money)

---

## 💡 **Pro Tips**

1. **Slow down** when showing RED alert - let judges read
2. **Use hand gestures** to point at screen
3. **Make eye contact** when saying "protects your money"
4. **Smile** when GREEN approval shows (positive energy)

---

## 📝 **Post-Demo Q&A Prep**

**Expected Questions:**

**Q: "How does it prevent false rejections?"**
A: "AI has 95% confidence threshold. Low confidence triggers manual review."

**Q: "Can admins override?"**
A: "Yes, but override is logged in audit trail for accountability."

**Q: "What if vendor changes wallet?"**
A: "Must go through whitelist update process with governance approval."

**Q: "How fast is this?"**
A: "2-3 seconds with Groq, 3-5 with GPT-4. Real-time for user."

---

<div align="center">

## 🎯 **Remember: REJECTION First!**

**Show the problem → Show the solution**

**Block the bad → Approve the good**

### **This is your winning strategy!** 🏆

</div>
