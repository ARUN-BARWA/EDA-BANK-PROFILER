from ..engines import BaseEngine
from typing import Any

def generate_sales_productivity(engine: BaseEngine, sales_table: str, targets_table: str) -> Any:
    query = f"""
    SELECT 
        s.sales_user_id,
        s.employee_code,
        s.role,
        s.branch_code as branch,
        s.region,
        t.target_accounts,
        t.achieved_accounts,
        (t.achieved_accounts * 100.0 / NULLIF(t.target_accounts, 0)) as target_achievement_percent,
        t.target_funded_accounts,
        t.achieved_funded_accounts,
        (t.achieved_funded_accounts * 100.0 / NULLIF(t.target_funded_accounts, 0)) as funded_achievement_percent,
        t.target_balance,
        t.achieved_balance
    FROM {sales_table} s
    JOIN {targets_table} t ON s.sales_user_id = t.sales_user_id
    """
    df = engine.execute_query(query)
    if not df.empty:
        df = df.round(2)
    return df
