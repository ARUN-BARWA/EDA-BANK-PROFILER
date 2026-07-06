import difflib
from typing import List, Dict

def suggest_column_mappings(available_columns: List[str], required_columns: List[str]) -> Dict[str, str]:
    """Uses fuzzy matching to suggest column mappings from available to required columns."""
    mappings = {}
    for req in required_columns:
        if req in available_columns:
            mappings[req] = req
        else:
            # simple fuzzy match
            matches = difflib.get_close_matches(req, available_columns, n=1, cutoff=0.6)
            if matches:
                mappings[req] = matches[0]
            else:
                # hardcoded common mappings fallback
                fallbacks = {
                    "account_open_date": ["acct_open_dt", "open_date", "opened_date"],
                    "avg_monthly_balance": ["avg_bal", "balance", "monthly_balance"],
                    "upi_enabled_flag": ["upi_flag", "is_upi"],
                    "first_funding_date": ["funded_dt", "first_fund_date"]
                }
                if req in fallbacks:
                    for fb in fallbacks[req]:
                        if fb in available_columns:
                            mappings[req] = fb
                            break
    return mappings
