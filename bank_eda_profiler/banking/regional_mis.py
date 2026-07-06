from ..engines import BaseEngine
from typing import Any

def generate_regional_mis(engine: BaseEngine, leads_table: str, accounts_table: str) -> Any:
    query = f"""
    WITH leads_agg AS (
        SELECT region, COUNT(lead_id) as leads
        FROM {leads_table}
        GROUP BY region
    ),
    acct_agg AS (
        SELECT 
            region, 
            COUNT(account_id) as accounts_opened,
            SUM(CASE WHEN first_funding_date IS NOT NULL THEN 1 ELSE 0 END) as funded_accounts,
            AVG(avg_monthly_balance) as average_balance,
            SUM(CASE WHEN first_transaction_date IS NOT NULL THEN 1 ELSE 0 END) as first_transaction_count,
            SUM(CASE WHEN upi_enabled_flag = True THEN 1 ELSE 0 END) as upi_active_count,
            SUM(CASE WHEN debit_card_issued_flag = True THEN 1 ELSE 0 END) as debit_card_active_count
        FROM {accounts_table}
        GROUP BY region
    )
    SELECT 
        l.region,
        l.leads,
        COALESCE(a.accounts_opened, 0) as accounts_opened,
        COALESCE(a.funded_accounts, 0) as funded_accounts,
        (COALESCE(a.funded_accounts, 0) * 100.0 / NULLIF(COALESCE(a.accounts_opened, 0), 0)) as activation_percent,
        COALESCE(a.average_balance, 0) as average_balance,
        COALESCE(a.first_transaction_count, 0) as first_transaction_count,
        COALESCE(a.upi_active_count, 0) as upi_active_count,
        COALESCE(a.debit_card_active_count, 0) as debit_card_active_count
    FROM leads_agg l
    LEFT JOIN acct_agg a ON l.region = a.region
    """
    df = engine.execute_query(query)
    if not df.empty:
        df = df.round(2)
    return df
