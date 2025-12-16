# 📄 MNEE Sentinel - PDF Invoice Parser Guide

## 🎯 Overview

The PDF parsing feature uses **Docling** to automatically extract payment information from uploaded invoices and contracts. This eliminates manual data entry and reduces errors.

---

## 🚀 Quick Start

### Installation

```bash
# Install Docling
pip install docling

# Or reinstall all requirements
pip install -r requirements.txt
```

---

## 💡 Use Cases

### 1. **Streamlit Dashboard (Interactive)**

Upload a PDF invoice in the web interface:

1. Go to **Tab 1: Submit Proposal**
2. Click **"Browse files"** under "Upload Invoice PDF"
3. Select your PDF invoice
4. Wait for parsing (2-5 seconds)
5. Review extracted data
6. Click "Use this proposal" or edit as needed

**Extracted Data:**
- ✅ Vendor name
- ✅ Invoice amount
- ✅ Invoice number
- ✅ Date
- ✅ Description

### 2. **Batch Processing (Command Line)**

Process multiple invoices at once:

```bash
# Process all PDFs in current folder
python process_invoices.py

# Process PDFs in specific folder
python process_invoices.py ./invoices

# Process and extract invoice data
python process_invoices.py ./invoices --extract

# Specify custom output folder
python process_invoices.py ./invoices -o results
```

**Output:**
- JSON files in `hasil_konversi/` folder
- Extracted data in `*_extracted.json` files

### 3. **Python Integration**

Use the parser in your own scripts:

```python
from utils.document_parser import InvoiceParser

# Initialize parser
parser = InvoiceParser()

# Parse single PDF
document_dict = parser.parse_pdf("invoice.pdf")

# Extract invoice data
extracted = parser.extract_invoice_data(document_dict)

print(f"Vendor: {extracted['vendor_name']}")
print(f"Amount: {extracted['amount']}")

# Generate proposal text
proposal = parser.generate_proposal_from_invoice(
    document_dict,
    wallet_address="0xABC..."
)
print(proposal)
```

---

## 📋 Supported PDF Formats

### ✅ Works Best With:

- **Standard invoices** (PDF format)
- **English or Indonesian** text
- **Clear structure** with headers
- **Typed text** (not handwritten)
- **Single-page** or multi-page documents

### ⚠️ Limited Support For:

- Scanned images (OCR quality dependent)
- Handwritten invoices
- Complex table structures
- Encrypted/password-protected PDFs

---

## 🔍 What Gets Extracted

### Automatic Extraction:

```json
{
  "vendor_name": "PT Nusantara FX Services",
  "amount": 50.00,
  "invoice_number": "INV-2024-001",
  "date": "15/12/2024",
  "category": null,
  "description": "FX hedging services for Q4 2024",
  "raw_text": "Full text content..."
}
```

### Extraction Patterns:

| Field | Pattern Examples |
|-------|-----------------|
| **Vendor** | PT Company Name, Inc., Ltd., Corp. |
| **Amount** | Total: $500, Rp 500,000, Amount: 500 |
| **Invoice #** | Invoice: INV-001, No. 12345 |
| **Date** | Date: 15/12/2024, 2024-12-15 |

---

## 🎨 Example Workflow

### Scenario: Process Vendor Invoice

**Step 1: Receive PDF Invoice**
```
Vendor sends: invoice_december_2024.pdf
```

**Step 2: Upload to Dashboard**
- Open MNEE Sentinel
- Go to Submit Proposal tab
- Upload PDF

**Step 3: Review Extracted Data**
```
✅ Extracted Data:
   Vendor: PT Cloud Treasury Tools
   Amount: 35.00 MNEE
   Invoice: INV-202412-045
```

**Step 4: AI Validation**
```
Auto-generated proposal:
"Transfer 35 MNEE to PT Cloud Treasury Tools 
for invoice INV-202412-045"
```

**Step 5: Submit for Audit**
- Click "Submit for AI Audit"
- AI validates against governance rules
- Execute if approved

---

## 🛠️ Advanced Usage

### Customize Extraction Logic

Edit `utils/document_parser.py`:

```python
def extract_invoice_data(self, document_dict: Dict) -> Dict:
    # Add custom extraction patterns
    
    # Example: Extract purchase order number
    po_match = re.search(r'PO[:\s#]*([A-Z0-9-]+)', raw_text)
    if po_match:
        extracted['po_number'] = po_match.group(1)
    
    return extracted
```

### Integrate with Database

Automatically save parsed invoices:

```python
# After parsing
document_dict = parser.parse_pdf("invoice.pdf")

# Save to database
db.client.table("parsed_invoices").insert({
    "filename": "invoice.pdf",
    "vendor_name": extracted['vendor_name'],
    "amount": extracted['amount'],
    "parsed_at": datetime.now().isoformat(),
    "raw_json": json.dumps(document_dict)
}).execute()
```

---

## 📊 Batch Processing Examples

### Process Monthly Invoices

```bash
# Folder structure:
invoices/
├── 2024-12-vendor1.pdf
├── 2024-12-vendor2.pdf
└── 2024-12-vendor3.pdf

# Process all
python process_invoices.py invoices --extract

# Output:
hasil_konversi/
├── 2024-12-vendor1.json
├── 2024-12-vendor1_extracted.json
├── 2024-12-vendor2.json
├── 2024-12-vendor2_extracted.json
└── ...
```

### Generate Proposals from Batch

```python
from utils.document_parser import InvoiceParser
import json
from pathlib import Path

parser = InvoiceParser()

# Process all invoices in folder
for pdf_file in Path("invoices").glob("*.pdf"):
    # Parse
    doc_dict = parser.parse_pdf(str(pdf_file))
    
    # Extract data
    extracted = parser.extract_invoice_data(doc_dict)
    
    # Generate proposal
    proposal = parser.generate_proposal_from_invoice(doc_dict)
    
    # Save to proposals list
    with open("proposals.txt", "a") as f:
        f.write(f"{proposal}\n")
    
    print(f"✅ Processed: {pdf_file.name}")
```

---

## 🔧 Troubleshooting

### Issue: "Docling not installed"

```bash
# Solution
pip install docling

# If that fails, try:
pip install --upgrade pip
pip install docling --no-cache-dir
```

### Issue: "Failed to parse PDF"

**Possible causes:**
- PDF is encrypted
- PDF is corrupted
- PDF is image-only (no text layer)

**Solutions:**
1. Use Adobe Acrobat to re-save PDF
2. Use OCR tool to add text layer
3. Convert to text-based PDF

### Issue: "Extracted data is incomplete"

**Solutions:**
1. Check PDF structure (is text selectable?)
2. Customize extraction patterns in `document_parser.py`
3. Use manual proposal entry as fallback

### Issue: "Memory error with large PDFs"

```python
# Process in smaller batches
parser = InvoiceParser()

# Process one at a time
for pdf in large_pdf_list:
    result = parser.parse_pdf(pdf)
    # Save immediately
    parser.save_parsed_result(result, f"{pdf}.json")
    del result  # Free memory
```

---

## 📈 Performance

### Benchmarks:

| PDF Size | Pages | Processing Time |
|----------|-------|----------------|
| 100 KB | 1 | 2-3 seconds |
| 500 KB | 5 | 5-8 seconds |
| 1 MB | 10 | 10-15 seconds |
| 5 MB | 50 | 30-60 seconds |

### Optimization Tips:

1. **Use smaller PDFs**: Split multi-page documents
2. **Batch overnight**: Process large batches during off-hours
3. **Cache results**: Save parsed JSON for reuse
4. **Use SSD**: Faster disk I/O helps

---

## 🔐 Security Considerations

### PDF Upload Safety:

- ✅ Files stored in temporary directory
- ✅ Automatically deleted after processing
- ✅ No persistent storage without user action
- ✅ Input validation on file type

### Best Practices:

```python
# Validate file size before upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

if uploaded_file.size > MAX_FILE_SIZE:
    st.error("File too large. Max 10 MB.")
```

---

## 🎓 Learning Resources

### Docling Documentation:
- GitHub: https://github.com/DS4SD/docling
- Docs: Check repository README

### Related Tools:
- **PyPDF2**: Basic PDF manipulation
- **pdfplumber**: Table extraction
- **Tesseract OCR**: Image-based PDFs

---

## 🚀 Future Enhancements

### Planned Features:

- [ ] Multi-language support (beyond EN/ID)
- [ ] Table extraction for line items
- [ ] Automatic vendor matching
- [ ] OCR for scanned documents
- [ ] PDF signature verification
- [ ] Bulk upload (multiple PDFs at once)

### Contributing:

Want to improve PDF parsing? Edit `utils/document_parser.py` and add:

1. Better regex patterns
2. ML-based extraction
3. Support for more invoice formats

---

## 📞 Support

### Questions?

- Check `document_parser.py` source code
- See example in `process_invoices.py`
- Review INSTALLATION_GUIDE.md

### Report Issues:

```bash
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run and capture logs
python process_invoices.py 2> error.log
```

---

<div align="center">

## ✅ PDF Parsing Ready!

**MNEE Sentinel** now supports intelligent invoice processing

Upload → Extract → Validate → Execute

</div>
