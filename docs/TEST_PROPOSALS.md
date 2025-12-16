# 🧪 MNEE Sentinel - Test Proposals

## Test scenarios for demo and development

---

## 🔴 **REJECTION Test Cases** (Show These FIRST!)

### **1. Budget Exceeded (HIGH RISK)**

**Proposal:**
```
Transfer 1000 MNEE to PT Cloud Treasury Tools (0xD4e5F60718293aBcD4E5F6071829AbcD4) for cloud services
```

**Expected Result:**
- ❌ REJECTED
- Reason: Insufficient budget (90 MNEE available, 1000 requested)
- Risk Level: HIGH
- Category: Software

---

### **2. Vendor Not Whitelisted (CRITICAL RISK)**

**Proposal:**
```
Transfer 50 MNEE to PT Hantu Consulting (0x0000000000000000000000000000000000000000) for advisory
```

**Expected Result:**
- ❌ REJECTED
- Reason: Vendor not in whitelist database
- Risk Level: CRITICAL
- Category: Unknown

---

### **3. Exceeds Vendor Limit**

**Proposal:**
```
Transfer 150 MNEE to PT Nusantara FX Services (0xA1b2C3D4e5F60718293aBcD4E5F6071829Ab) for FX hedging
```

**Expected Result:**
- ❌ REJECTED
- Reason: Amount 150 > Vendor limit 100 MNEE
- Risk Level: HIGH
- Category: FX

---

### **4. Invalid Address Format**

**Proposal:**
```
Transfer 50 MNEE to PT Valid Company (0xINVALID_ADDRESS) for services
```

**Expected Result:**
- ❌ REJECTED
- Reason: Invalid Ethereum address format
- Risk Level: MEDIUM
- Category: Parsing error

---

### **5. Insufficient Information (Low Confidence)**

**Proposal:**
```
Send money to vendor for stuff
```

**Expected Result:**
- ❌ REJECTED
- Reason: Cannot parse with sufficient confidence
- Risk Level: MEDIUM
- AI Confidence: < 70%

---

## 🟢 **APPROVAL Test Cases** (Show After Rejections)

### **1. Valid FX Transaction**

**Proposal:**
```
Transfer 50 MNEE to PT Nusantara FX Services (0xA1b2C3D4e5F60718293aBcD4E5F6071829Ab) for FX hedging
```

**Expected Result:**
- ✅ APPROVED
- All checks passed
- Risk Level: LOW
- Category: FX
- Budget: 200 MNEE available

---

### **2. Valid Remittance**

**Proposal:**
```
Pay PT Global Money Transfer 40 MNEE at address 0xB2c3D4E5F60718293aBcD4E5F6071829Abc for remittance services
```

**Expected Result:**
- ✅ APPROVED
- Vendor limit: 50 MNEE (within limit)
- Budget: 120 MNEE available
- Category: Remittance

---

### **3. Valid Office Supplies**

**Proposal:**
```
Send 25 MNEE to PT Office Supplies Jakarta (0x0718293aBcD4E5F6071829AbcD4E5F607) for stationery
```

**Expected Result:**
- ✅ APPROVED
- Small amount, low risk
- Category: Office
- Budget: 40 MNEE available

---

### **4. Valid Cybersecurity**

**Proposal:**
```
Transfer 30 MNEE to PT Cybersecurity Services (0x293aBcD4E5F6071829AbcD4E5F607182) for monthly security audit
```

**Expected Result:**
- ✅ APPROVED
- Category: Cybersecurity
- Budget: 110 MNEE available
- Vendor limit: 50 MNEE

---

## 🎯 **Demo Sequence** (Recommended Order)

### **Phase 1: Show Protection (3 test cases)**
1. Budget Exceeded → 🔴 BLOCKED
2. Vendor Not Whitelisted → 🔴 BLOCKED  
3. Exceeds Vendor Limit → 🔴 BLOCKED

**Pause and emphasize:** "AI protects your money!"

### **Phase 2: Show Approval (1-2 test cases)**
4. Valid FX Transaction → 🟢 APPROVED
5. (Optional) Valid Office Supplies → 🟢 APPROVED

**Emphasis:** "AI is smart, not paranoid. Valid = Fast approval."

---

## 📊 **Edge Cases** (For Q&A)

### **Borderline Amount**

**Proposal:**
```
Transfer 90 MNEE to PT Cloud Treasury Tools (0xD4e5F60718293aBcD4E5F60718293aBcD4E5F607) for cloud services
```

**Expected:**
- ✅ APPROVED (exactly at budget limit)
- Shows: 90/90 MNEE used (100%)

---

### **Multiple Vendors, Same Category**

**Proposal 1:**
```
Transfer 50 MNEE to PT Nusantara FX Services for hedging
```
(✅ APPROVED)

**Proposal 2:**
```
Transfer 50 MNEE to another FX vendor
```
(❌ REJECTED - Second vendor not whitelisted)

**Shows:** Whitelist enforcement works

---

## 🧪 **Stress Test Scenarios** (Optional)

### **Velocity Test**
Run same proposal 11 times in quick succession.

**Expected:**
- First 10: ✅ APPROVED
- 11th: ❌ REJECTED (velocity limit)

---

### **Budget Depletion**

**Sequence:**
1. Transfer 50 MNEE (✅ APPROVED) - 40 left
2. Transfer 40 MNEE (✅ APPROVED) - 0 left  
3. Transfer 10 MNEE (❌ REJECTED) - No budget

---

## 📝 **Copy-Paste Ready** (For Quick Demo)

### **🔴 Rejection Example:**
```
Transfer 1000 MNEE to PT Cloud Treasury Tools (0xD4e5F60718293aBcD4E5F60718293aBcD4E5F607) for cloud services
```

### **🟢 Approval Example:**
```
Transfer 50 MNEE to PT Nusantara FX Services (0xA1b2C3D4e5F60718293aBcD4E5F60718293aBcD4) for FX hedging
```

---

## 🎬 **Demo Tips**

1. **Keep proposals ready** in a text file
2. **Copy-paste** for speed (don't type live)
3. **Use rejection first** to show protection
4. **Show 2-3 rejections** then 1 approval
5. **Point out risk levels** on screen

---

## 📋 **Expected AI Responses**

### **For Rejections:**
```
🚫 TRANSACTION BLOCKED
Risk Level: HIGH/CRITICAL
AI Confidence: 90-95%

Detailed Reasoning:
- What went wrong
- Numbers/evidence
- Specific rule violated
```

### **For Approvals:**
```
✅ APPROVED
Risk Level: LOW
AI Confidence: 90-95%

All Checks Passed:
✓ Vendor whitelisted
✓ Within limits
✓ Budget available
✓ Velocity OK
```

---

## 🔍 **Verification After Each Test**

### **Check Audit Log:**
1. Go to Tab 3
2. Find latest entry
3. Verify:
   - Decision matches expected
   - Reasoning is detailed
   - Confidence score shown
   - Timestamp recorded

---

<div align="center">

## 💡 **Remember:**

**Show WHAT IT BLOCKS before showing what it approves!**

**Rejection = Protection = Value**

</div>
