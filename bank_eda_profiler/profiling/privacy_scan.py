import re
from typing import List, Dict

def scan_for_pii(columns: List[str]) -> Dict[str, str]:
    """Scans column names (and potentially data) for PII patterns."""
    pii_warnings = {}
    
    # Simple regex based on column names for now
    patterns = {
        "mobile": re.compile(r"mobile|phone|contact_no", re.IGNORECASE),
        "email": re.compile(r"email", re.IGNORECASE),
        "pan": re.compile(r"pan_no|pan_number", re.IGNORECASE),
        "aadhaar": re.compile(r"aadhaar", re.IGNORECASE),
        "name": re.compile(r"name", re.IGNORECASE),
        "account_number": re.compile(r"account_no|acct_no", re.IGNORECASE),
    }
    
    for col in columns:
        for pii_type, pattern in patterns.items():
            if pattern.search(col):
                pii_warnings[col] = f"Potential {pii_type} found"
                break
                
    return pii_warnings
