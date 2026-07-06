import pytest
from bank_eda_profiler.io.column_mapping import suggest_column_mappings

def test_column_mappings():
    available = ["acct_open_dt", "avg_bal", "upi_flag", "other_col"]
    required = ["account_open_date", "avg_monthly_balance", "upi_enabled_flag", "missing_col"]
    
    mappings = suggest_column_mappings(available, required)
    
    assert mappings["account_open_date"] == "acct_open_dt"
    assert mappings["avg_monthly_balance"] == "avg_bal"
    assert mappings["upi_enabled_flag"] == "upi_flag"
    assert "missing_col" not in mappings
