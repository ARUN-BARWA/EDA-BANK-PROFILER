from ..engines import BaseEngine
from typing import Any

def generate_dormancy_report(engine: BaseEngine, accounts_table: str) -> Any:
    query = f"""
    SELECT 
        customer_id,
        account_id,
        region,
        branch_code,
        account_open_date,
        first_funding_date,
        first_transaction_date,
        last_transaction_date,
        current_balance,
        CASE WHEN current_date - last_transaction_date > 30 THEN True ELSE False END as dormant_30_flag,
        CASE WHEN current_date - last_transaction_date > 60 THEN True ELSE False END as dormant_60_flag,
        CASE WHEN current_date - last_transaction_date > 90 THEN True ELSE False END as dormant_90_flag,
        CASE WHEN first_funding_date IS NULL THEN True ELSE False END as opened_but_never_funded_flag,
        CASE WHEN first_funding_date IS NOT NULL AND first_transaction_date IS NULL THEN True ELSE False END as funded_but_never_transacted_flag
    FROM {accounts_table}
    """
    return engine.execute_query(query)
