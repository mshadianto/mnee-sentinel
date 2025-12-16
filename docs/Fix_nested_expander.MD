# 🔧 Fix: Nested Expander Error in app.py

## ❌ Error Message
```
StreamlitAPIException: Expanders may not be nested inside other expanders.
File "app.py", line 804: with st.expander("📄 Original Proposal Text"):
```

## ✅ How to Fix

Open `app.py` and find **lines 803-805** (around line 803-805):

### 🔴 FIND THIS CODE (Delete these lines):
```python
                # Show original proposal
                with st.expander("📄 Original Proposal Text"):
                    st.code(audit.get('proposal_text', 'N/A'), language=None)
```

### 🟢 REPLACE WITH THIS:
```python
                # Show original proposal (checkbox toggle instead of nested expander)
                if st.checkbox(f"📄 Show Original Proposal", key=f"proposal_{audit['id']}"):
                    st.code(audit.get('proposal_text', 'N/A'), language=None)
```

---

## 📋 Alternative Fix (Simpler - Just Show It)

If the checkbox doesn't work, use this even simpler version:

### 🟢 REPLACE WITH:
```python
                # Show original proposal
                st.markdown("**📄 Original Proposal Text:**")
                st.code(audit.get('proposal_text', 'N/A'), language=None)
```

---

## 🔄 After Fixing

1. Save `app.py`
2. Restart Streamlit:
   ```bash
   # Stop with Ctrl+C, then:
   python -m streamlit run app.py
   ```

---

## 💡 Why This Happened

Streamlit v1.29+ doesn't allow putting an `st.expander()` inside another `st.expander()`. 

The code had:
- Outer expander: Line 769 (for each audit entry)
- Inner expander: Line 804 (for proposal text) ← PROBLEM

The fix removes the inner expander and uses a checkbox or just displays the text directly.