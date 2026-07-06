REPORT_REQUIREMENTS = {
    "activation_quality_report": {
        "required_tables": ["accounts"],
        "optional_tables": ["sales"],
        "required_fields": {
            "accounts": [
                "account_id",
                "customer_id",
                "account_open_date",
                "region",
                "branch_code",
                "first_transaction_date",
                "avg_monthly_balance"
            ]
        },
        "optional_fields": {
            "accounts": [
                "first_funding_date",
                "initial_funding_amount",
                "upi_enabled_flag",
                "debit_card_issued_flag",
                "mobile_banking_active"
            ]
        },
        "fallback_rules": {
            "funded_accounts": "Use first_funding_date if available, otherwise use initial_funding_amount > 0.",
            "upi_active": "Requires upi_enabled_flag or a mapped equivalent column.",
            "debit_card_active": "Use debit_card_issued_flag or virtual_card_active_flag if available."
        }
    },
    "kyc_dropoff_report": {
        "required_tables": ["applications", "vkyc"],
        "required_fields": {
            "applications": ["application_id", "vkyc_required_flag"],
            "vkyc": ["application_id", "status"]
        }
    },
    "salesperson_productivity_report": {
        "required_tables": ["leads", "applications", "accounts", "sales", "targets"],
        "required_fields": {
            "sales": ["sales_user_id"]
        }
    }
}
