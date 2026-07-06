from ..engines import BaseEngine
from typing import Any
import pandas as pd

def generate_activation_quality(engine: BaseEngine, accounts_table: str) -> Any:
    query = f"""
    SELECT 
        region,
        branch_code,
        COUNT(account_id) as accounts_opened,
        SUM(CASE WHEN first_funding_date IS NOT NULL THEN 1 ELSE 0 END) as first_funding_done,
        SUM(CASE WHEN first_transaction_date IS NOT NULL THEN 1 ELSE 0 END) as first_transaction_done,
        SUM(CASE WHEN upi_enabled_flag = True THEN 1 ELSE 0 END) as upi_active,
        SUM(CASE WHEN debit_card_issued_flag = True THEN 1 ELSE 0 END) as debit_card_active,
        SUM(CASE WHEN mobile_banking_active = True THEN 1 ELSE 0 END) as mobile_banking_active,
        AVG(avg_monthly_balance) as average_balance
    FROM {accounts_table}
    GROUP BY region, branch_code
    """
    df = engine.execute_query(query)
    
    if not df.empty:
        df["funded_account_percent"] = (df["first_funding_done"] / df["accounts_opened"]) * 100
        df["first_transaction_percent"] = (df["first_transaction_done"] / df["accounts_opened"]) * 100
        df["upi_activation_percent"] = (df["upi_active"] / df["accounts_opened"]) * 100
        df["debit_card_activation_percent"] = (df["debit_card_active"] / df["accounts_opened"]) * 100
        
        # Round decimals
        df = df.round(2)
        
    return df
