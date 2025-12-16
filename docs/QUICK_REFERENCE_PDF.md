# 📄 PDF Invoice Parser - Quick Reference

## 🚀 3 Ways to Use

### 1️⃣ Web Interface (Easiest)
```
1. Open Streamlit dashboard
2. Go to "Submit Proposal" tab
3. Upload PDF invoice
4. Click "Submit for AI Audit"
```

### 2️⃣ Command Line (Batch)
```bash
# Process all PDFs in folder
python process_invoices.py ./invoices --extract

# Output: JSON files with extracted data
```

### 3️⃣ Python Script (Custom)
```python
from utils.document_parser import InvoiceParser

parser = InvoiceParser()
data = parser.parse_pdf("invoice.pdf")
extracted = parser.extract_invoice_data(data)
```

---

## 📋 What Gets Extracted

```json
{
  "vendor_name": "PT Company Name",
  "amount": 50.00,
  "invoice_number": "INV-2024-001",
  "date": "15/12/2024",
  "description": "Services rendered..."
}
```

---

## ⚡ Quick Tips

✅ **Best Results:**
- PDF with selectable text
- Clear invoice structure
- Standard format

⚠️ **May Need Manual Review:**
- Scanned images
- Handwritten invoices
- Complex layouts

---

## 🔧 Installation

```bash
pip install docling
```

---

## 📚 Documentation

- **Full Guide**: See `PDF_PARSING_GUIDE.md`
- **Source Code**: `utils/document_parser.py`
- **CLI Tool**: `process_invoices.py`

---

## 💡 Example

**Input PDF:**
```
INVOICE #12345
Date: December 15, 2024

Bill To: Your Company
From: PT Vendor ABC

Description: Cloud Services
Amount: $500.00
```

**Extracted:**
```python
{
  'vendor_name': 'PT Vendor ABC',
  'amount': 500.00,
  'invoice_number': '12345',
  'date': '15/12/2024'
}
```

**Auto-Generated Proposal:**
```
"Transfer 500 MNEE to PT Vendor ABC for invoice 12345"
```

---

<div align="center">

**Ready to Use!**

Upload an invoice and try it now! 🎉

</div>
