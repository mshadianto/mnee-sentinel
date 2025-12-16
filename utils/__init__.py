"""
MNEE Sentinel Utilities
"""

# Import from document_parser - using correct class name
try:
    from .document_parser import InvoiceParser, batch_process_pdfs, get_parser_status
    # Alias for backward compatibility
    FastInvoiceParser = InvoiceParser
    
    def parse_uploaded_pdf(uploaded_file):
        """Convenience function for parsing uploaded PDF"""
        parser = InvoiceParser()
        return parser.parse_uploaded_file(uploaded_file)
        
except ImportError:
    # If document_parser not available, provide dummy
    InvoiceParser = None
    FastInvoiceParser = None
    parse_uploaded_pdf = None
    batch_process_pdfs = None
    get_parser_status = None

# Import other utilities
from .crypto_utils import MNEETokenManager
from .db_utils import GovernanceDB

__all__ = [
    'InvoiceParser',
    'FastInvoiceParser', 
    'parse_uploaded_pdf', 
    'batch_process_pdfs',
    'get_parser_status',
    'MNEETokenManager',
    'GovernanceDB'
]