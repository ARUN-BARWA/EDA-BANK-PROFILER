import pytest
from bank_eda_profiler.profiling.privacy_scan import scan_for_pii

def test_privacy_scan():
    cols = ["customer_id", "mobile_hash", "raw_mobile_no", "email_address", "pan_number", "balance"]
    warnings = scan_for_pii(cols)
    
    assert "raw_mobile_no" in warnings
    assert "email_address" in warnings
    assert "pan_number" in warnings
    assert "balance" not in warnings
