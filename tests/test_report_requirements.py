import pytest
from bank_eda_profiler.banking.readiness import ReadinessReport, check_requirements
from bank_eda_profiler.banking.report_requirements import REPORT_REQUIREMENTS

def test_check_requirements():
    available_tables = ["accounts", "sales"]
    available_schemas = {
        "accounts": ["account_id", "customer_id", "account_open_date", "region", "branch_code", "first_transaction_date", "avg_monthly_balance"]
    }
    
    # Missing sales required fields
    res = check_requirements("activation_quality_report", available_tables, available_schemas)
    assert res.status == "READY"
    assert res.score == 100.0

def test_missing_table():
    res = check_requirements("kyc_dropoff_report", ["applications"], {})
    assert res.status == "NOT_READY"
    assert "vkyc" in res.details["required_tables_missing"]
