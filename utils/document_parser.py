"""
Fast PDF Invoice Parser for MNEE Sentinel
Uses PyMuPDF (fitz) for fast extraction - typically <1 second vs 1+ minute with Docling

Install: pip install pymupdf

Compatible with existing app.py interface:
- InvoiceParser class
- parse_uploaded_file() method
- extract_invoice_data() method  
- generate_proposal_from_invoice() method
"""

import re
import json
import logging
import tempfile
import os
from pathlib import Path
from typing import Dict, Optional, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Try PyMuPDF first (FAST!)
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
    logger.info("✅ PyMuPDF available - fast PDF parsing enabled")
except ImportError:
    fitz = None
    PYMUPDF_AVAILABLE = False
    logger.warning("⚠️ PyMuPDF not installed. Run: pip install pymupdf")

# Docling as fallback (SLOW - not recommended)
try:
    from docling.document_converter import DocumentConverter
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    DocumentConverter = None


class InvoiceParser:
    """
    Fast PDF invoice parser optimized for treasury proposals.
    
    Speed comparison:
    - PyMuPDF: ~0.1-0.5 seconds ✅
    - Docling: ~30-90 seconds ❌
    
    Usage:
        parser = InvoiceParser()
        doc = parser.parse_uploaded_file(uploaded_file)
        data = parser.extract_invoice_data(doc)
        proposal = parser.generate_proposal_from_invoice(doc)
    """
    
    def __init__(self, use_docling: bool = False):
        """
        Initialize parser.
        
        Args:
            use_docling: Force use Docling (slower but handles complex layouts)
        """
        self.use_docling = use_docling and DOCLING_AVAILABLE
        
        if self.use_docling:
            self.converter = DocumentConverter()
            logger.info("📄 Using Docling parser (slower)")
        elif PYMUPDF_AVAILABLE:
            logger.info("⚡ Using PyMuPDF parser (fast)")
        else:
            logger.warning("⚠️ No PDF parser available!")
    
    def parse_uploaded_file(self, uploaded_file) -> Dict:
        """
        Parse a Streamlit uploaded file.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Dictionary with parsed content
        """
        start_time = datetime.now()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        try:
            result = self.parse_pdf(tmp_path)
            result['filename'] = uploaded_file.name
            result['file_size'] = uploaded_file.size
            
            elapsed = (datetime.now() - start_time).total_seconds()
            result['parse_time_seconds'] = elapsed
            logger.info(f"⚡ PDF parsed in {elapsed:.2f} seconds")
            
            return result
            
        finally:
            # Cleanup temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
    
    def parse_pdf(self, pdf_path: str) -> Dict:
        """
        Parse PDF file and extract text.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with raw_text, pages, etc.
        """
        if self.use_docling:
            return self._parse_with_docling(pdf_path)
        elif PYMUPDF_AVAILABLE:
            return self._parse_with_pymupdf(pdf_path)
        else:
            return self._parse_fallback(pdf_path)
    
    def _parse_with_pymupdf(self, pdf_path: str) -> Dict:
        """Fast parsing with PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            
            full_text = ""
            pages = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                full_text += text + "\n"
                pages.append({
                    "page_number": page_num + 1,
                    "text": text
                })
            
            doc.close()
            
            return {
                "status": "success",
                "parser": "pymupdf",
                "raw_text": full_text,
                "pages": pages,
                "page_count": len(pages),
                "file_path": str(pdf_path)
            }
            
        except Exception as e:
            logger.error(f"PyMuPDF parsing failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "raw_text": "",
                "parser": "pymupdf"
            }
    
    def _parse_with_docling(self, pdf_path: str) -> Dict:
        """Slower parsing with Docling"""
        try:
            result = self.converter.convert(pdf_path)
            document_dict = result.document.export_to_dict()
            
            # Extract raw text
            raw_text = ""
            if "texts" in document_dict:
                for text_item in document_dict["texts"]:
                    if "text" in text_item:
                        raw_text += text_item["text"] + "\n"
            
            return {
                "status": "success",
                "parser": "docling",
                "raw_text": raw_text,
                "document": document_dict,
                "file_path": str(pdf_path)
            }
            
        except Exception as e:
            logger.error(f"Docling parsing failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "raw_text": "",
                "parser": "docling"
            }
    
    def _parse_fallback(self, pdf_path: str) -> Dict:
        """Fallback when no parser available"""
        return {
            "status": "error",
            "parser": "none",
            "raw_text": "",
            "error": "No PDF parser installed. Run: pip install pymupdf"
        }
    
    def extract_invoice_data(self, document_dict: Dict) -> Dict:
        """
        Extract structured invoice data from parsed document.
        
        Args:
            document_dict: Result from parse_pdf() or parse_uploaded_file()
            
        Returns:
            Dictionary with vendor_name, amount, invoice_number, date, category, description
        """
        raw_text = document_dict.get("raw_text", "")
        
        if not raw_text:
            return {
                "vendor_name": None,
                "amount": None,
                "invoice_number": None,
                "date": None,
                "category": None,
                "description": None,
                "extraction_confidence": 0.0
            }
        
        extracted = {
            "vendor_name": self._extract_vendor(raw_text),
            "amount": self._extract_amount(raw_text),
            "invoice_number": self._extract_invoice_number(raw_text),
            "date": self._extract_date(raw_text),
            "category": self._detect_category(raw_text),
            "description": self._extract_description(raw_text),
            "raw_text_preview": raw_text[:500] + "..." if len(raw_text) > 500 else raw_text
        }
        
        # Calculate confidence
        fields_found = sum(1 for v in [extracted["vendor_name"], extracted["amount"], 
                                        extracted["invoice_number"]] if v)
        extracted["extraction_confidence"] = fields_found / 3.0
        
        return extracted
    
    def _extract_vendor(self, text: str) -> Optional[str]:
        """Extract vendor/company name"""
        patterns = [
            # Indonesian company formats
            r'(?:PT|CV|UD|Firma|Yayasan)\.?\s+([A-Za-z][A-Za-z\s&.,\-]+?)(?:\n|,|\s{2,}|$)',
            # English company formats  
            r'(?:From|Vendor|Company|Supplier|Bill From)[:\s]+([A-Za-z][A-Za-z\s&.,\-]+?)(?:\n|$)',
            # Generic patterns
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|LLC|Ltd|Corp|Company|Services|Solutions)\.?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                vendor = match.group(1).strip()
                vendor = re.sub(r'\s+', ' ', vendor)
                if 3 < len(vendor) < 100:
                    return vendor
        
        return None
    
    def _extract_amount(self, text: str) -> Optional[float]:
        """Extract payment amount"""
        patterns = [
            # MNEE token
            r'([\d.,]+)\s*MNEE',
            # Indonesian Rupiah
            r'(?:Rp|IDR)\.?\s*([\d.,]+)',
            # USD/Dollar
            r'\$\s*([\d.,]+)',
            r'(?:USD|US\$)\s*([\d.,]+)',
            # Generic total patterns
            r'(?:Total|Amount|Jumlah|Grand Total|Subtotal)[:\s]*(?:Rp|IDR|\$|MNEE)?\s*([\d.,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '').replace(' ', '')
                try:
                    amount = float(amount_str)
                    if 0 < amount < 1_000_000_000:
                        return amount
                except ValueError:
                    continue
        
        return None
    
    def _extract_invoice_number(self, text: str) -> Optional[str]:
        """Extract invoice number"""
        patterns = [
            r'(?:Invoice|Inv|Faktur|No)[.:\s#]*([A-Z0-9][-A-Z0-9/]+)',
            r'(?:Number|Nomor)[:\s]*([A-Z0-9][-A-Z0-9/]+)',
            r'INV[-/]?(\d+[-/]?\d*)',
            r'#\s*([A-Z0-9][-A-Z0-9/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                inv_num = match.group(1).strip()
                if 3 <= len(inv_num) <= 30:
                    return inv_num
        
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract invoice date"""
        patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})',
            r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})',
            r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _detect_category(self, text: str) -> Optional[str]:
        """Detect expense category"""
        text_lower = text.lower()
        
        categories = {
            "FX": ["fx", "foreign exchange", "forex", "hedging", "currency"],
            "Remittance": ["remittance", "transfer", "wire", "payment"],
            "Settlement": ["settlement", "clearing", "reconciliation"],
            "Software": ["software", "license", "subscription", "saas", "cloud"],
            "Consulting": ["consulting", "advisory", "consultant", "professional"],
            "Travel": ["travel", "flight", "hotel", "transport", "accommodation"],
            "Office": ["office", "supplies", "stationery", "equipment"],
            "Data": ["data", "analytics", "market data", "feed", "api"],
            "Cybersecurity": ["security", "cyber", "firewall", "antivirus", "penetration"],
            "Legal": ["legal", "law", "attorney", "compliance", "regulatory"],
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return None
    
    def _extract_description(self, text: str) -> Optional[str]:
        """Extract service description"""
        patterns = [
            r'(?:Description|Deskripsi|Service|For)[:\s]+([^\n]+)',
            r'(?:RE|Subject|Perihal)[:\s]+([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                desc = match.group(1).strip()
                if len(desc) > 5:
                    return desc[:200]
        
        return None
    
    def generate_proposal_from_invoice(self, document_dict: Dict, wallet_address: str = None) -> str:
        """
        Generate treasury proposal text from parsed invoice.
        
        Args:
            document_dict: Result from parse_pdf() or parse_uploaded_file()
            wallet_address: Optional vendor wallet address
            
        Returns:
            Natural language proposal string
        """
        extracted = self.extract_invoice_data(document_dict)
        
        vendor = extracted.get("vendor_name") or "Unknown Vendor"
        amount = extracted.get("amount") or 0
        invoice = extracted.get("invoice_number") or "N/A"
        description = extracted.get("description") or "Payment"
        
        address = wallet_address or "0x0000000000000000000000000000000000000000"
        
        proposal = f"Transfer {amount} MNEE to {vendor} for invoice {invoice}. Description: {description}"
        
        return proposal


# ===================================
# Batch Processing
# ===================================

def batch_process_pdfs(folder_path: str, output_folder: str = "hasil_konversi") -> List[str]:
    """Process all PDFs in a folder"""
    folder = Path(folder_path)
    output = Path(output_folder)
    output.mkdir(exist_ok=True)
    
    parser = InvoiceParser()
    saved_files = []
    
    pdf_files = list(folder.glob("*.pdf")) + list(folder.glob("*.PDF"))
    
    if not pdf_files:
        print(f"⚠️ No PDF files found in {folder_path}")
        return saved_files
    
    print(f"📄 Found {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        try:
            print(f"\n🔄 Processing: {pdf_file.name}")
            
            parsed = parser.parse_pdf(str(pdf_file))
            
            # Save JSON
            json_file = output / f"{pdf_file.stem}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(parsed, f, indent=2, ensure_ascii=False)
            
            saved_files.append(str(json_file))
            print(f"   ✅ Saved: {json_file}")
            
            # Extract data
            extracted = parser.extract_invoice_data(parsed)
            print(f"   📊 Vendor: {extracted.get('vendor_name', 'N/A')}")
            print(f"   💰 Amount: {extracted.get('amount', 'N/A')}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return saved_files


# ===================================
# Check parser availability
# ===================================

def get_parser_status() -> Dict:
    """Get status of available parsers"""
    return {
        "pymupdf_available": PYMUPDF_AVAILABLE,
        "docling_available": DOCLING_AVAILABLE,
        "recommended": "pymupdf" if PYMUPDF_AVAILABLE else ("docling" if DOCLING_AVAILABLE else "none"),
        "install_command": "pip install pymupdf" if not PYMUPDF_AVAILABLE else None
    }


if __name__ == "__main__":
    print("⚡ Fast Invoice Parser for MNEE Sentinel")
    print("=" * 50)
    status = get_parser_status()
    print(f"PyMuPDF: {'✅' if status['pymupdf_available'] else '❌'}")
    print(f"Docling: {'✅' if status['docling_available'] else '❌'}")
    print(f"Recommended: {status['recommended']}")
    if status['install_command']:
        print(f"\n⚠️ Install with: {status['install_command']}")