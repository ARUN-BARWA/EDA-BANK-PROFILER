from ..engines import BaseEngine
from typing import Any

def generate_segmentation(engine: BaseEngine, accounts_table: str) -> Any:
    query = f"""
    SELECT 
        CASE 
            WHEN avg_monthly_balance >= 50000 THEN 'Elite'
            WHEN avg_monthly_balance >= 10000 THEN 'Prime'
            ELSE 'Mass'
        END as balance_segment,
        CASE
            WHEN first_funding_date IS NOT NULL THEN 'Funded'
            ELSE 'Unfunded'
        END as funding_segment,
        CASE
            WHEN current_date - last_transaction_date > 90 THEN 'Dormant'
            ELSE 'Active'
        END as activity_segment,
        COUNT(account_id) as customer_count,
        AVG(avg_monthly_balance) as avg_segment_balance
    FROM {accounts_table}
    GROUP BY 1, 2, 3
    ORDER BY customer_count DESC
    """
    df = engine.execute_query(query)
    if not df.empty:
        df = df.round(2)
    return df
