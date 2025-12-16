#!/usr/bin/env python3
"""
PDF Invoice Processor for MNEE Sentinel
Batch process PDF invoices and convert to structured JSON

Based on: tes_docling.py (original user script)
Enhanced with: Invoice data extraction for treasury management

Usage:
    python process_invoices.py [folder_path]
    
Example:
    python process_invoices.py ./invoices
"""

import os
import sys
import argparse
from pathlib import Path

# Import from MNEE Sentinel utils
from utils.document_parser import InvoiceParser


def main():
    parser = argparse.ArgumentParser(
        description='Process PDF invoices and extract payment data'
    )
    parser.add_argument(
        'folder',
        nargs='?',
        default='.',
        help='Folder containing PDF files (default: current directory)'
    )
    parser.add_argument(
        '-o', '--output',
        default='hasil_konversi',
        help='Output folder name (default: hasil_konversi)'
    )
    parser.add_argument(
        '--extract',
        action='store_true',
        help='Also extract invoice data (vendor, amount, etc.)'
    )
    
    args = parser.parse_args()
    
    # Validate folder
    folder_path = Path(args.folder).resolve()
    if not folder_path.exists():
        print(f"❌ Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    # Initialize parser
    print("🛡️  MNEE Sentinel - Invoice Processor")
    print("=" * 50)
    print(f"📂 Folder: {folder_path}")
    print(f"💾 Output: {args.output}")
    print(f"🔍 Extract Data: {'Yes' if args.extract else 'No'}")
    print("=" * 50)
    print()
    
    try:
        invoice_parser = InvoiceParser()
    except ImportError:
        print("❌ Error: Docling not installed")
        print("Install with: pip install docling")
        sys.exit(1)
    
    # Process all PDFs
    saved_files = invoice_parser.batch_process_pdfs(
        str(folder_path),
        args.output
    )
    
    # If extract flag is set, also extract invoice data
    if args.extract and saved_files:
        print("\n📊 Extracting invoice data...")
        print("-" * 50)
        
        for json_file in saved_files:
            try:
                import json
                with open(json_file, 'r', encoding='utf-8') as f:
                    document_dict = json.load(f)
                
                # Extract data
                extracted = invoice_parser.extract_invoice_data(document_dict)
                
                # Display
                print(f"\n📄 {Path(json_file).stem}:")
                print(f"   Vendor: {extracted.get('vendor_name', 'N/A')}")
                print(f"   Amount: {extracted.get('amount', 'N/A')}")
                print(f"   Invoice #: {extracted.get('invoice_number', 'N/A')}")
                print(f"   Date: {extracted.get('date', 'N/A')}")
                
                # Save extracted data
                extract_file = json_file.replace('.json', '_extracted.json')
                with open(extract_file, 'w', encoding='utf-8') as f:
                    json.dump(extracted, f, indent=2, ensure_ascii=False)
                print(f"   ✅ Saved to: {extract_file}")
                
            except Exception as e:
                print(f"   ⚠️ Error extracting: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Processing complete!")
    print(f"📁 Results saved to: {folder_path / args.output}")
    print("=" * 50)


if __name__ == "__main__":
    main()
