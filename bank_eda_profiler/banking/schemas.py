# Pre-defined schemas of tables like lead_master, account_master, etc.
# These act as reference logical schemas for the missing-field analyzer and Entity Detection Engine.

SCHEMAS = {
    "leads": ["lead_id", "mobile_hash", "lead_created_at", "region", "lead_status"],
    "accounts": [
        "account_id", "customer_id", "account_open_date", "region", "branch_code",
        "first_transaction_date", "avg_monthly_balance", "first_funding_date",
        "initial_funding_amount", "upi_enabled_flag", "debit_card_issued_flag",
        "mobile_banking_active"
    ],
    "applications": ["application_id", "lead_id", "status", "vkyc_required_flag", "application_start_time", "otp_verified_flag", "pan_verified_flag", "vkyc_completed_time", "account_opened_flag"],
    "vkyc": ["application_id", "status"],
    "sales": ["sales_user_id", "region", "branch"],
    "targets": ["sales_user_id", "target_amount"],
    "transactions": ["transaction_id", "account_id", "amount", "transaction_date", "transaction_type"],
    "campaigns": ["campaign_id", "campaign_name", "start_date", "end_date", "target_audience"]
}
