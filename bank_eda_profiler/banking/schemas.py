# Placeholder for pre-defined schemas of tables like lead_master, account_master, etc.
# These act as reference logical schemas for the missing-field analyzer.

SCHEMAS = {
    "leads": ["lead_id", "mobile_hash", "lead_created_at", "region", "lead_status"],
    "accounts": ["account_id", "customer_id", "account_open_date", "avg_monthly_balance"]
}
