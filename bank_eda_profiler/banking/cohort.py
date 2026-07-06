from ..engines import BaseEngine
from typing import Any

def generate_cohort(engine: BaseEngine, table: str, cohort_col: str, activity_col: str) -> Any:
    query = f"""
    WITH cohort_data AS (
        SELECT 
            customer_id,
            DATE_TRUNC('month', {cohort_col}) as cohort_month,
            DATE_TRUNC('month', {activity_col}) as activity_month
        FROM {table}
        WHERE {cohort_col} IS NOT NULL AND {activity_col} IS NOT NULL
    ),
    cohort_sizes AS (
        SELECT cohort_month, COUNT(DISTINCT customer_id) as customers_in_cohort
        FROM cohort_data
        GROUP BY cohort_month
    ),
    retention AS (
        SELECT 
            cohort_month,
            activity_month,
            COUNT(DISTINCT customer_id) as active_customers,
            date_diff('month', cohort_month, activity_month) as period_number
        FROM cohort_data
        GROUP BY cohort_month, activity_month
    )
    SELECT 
        r.cohort_month,
        r.period_number,
        s.customers_in_cohort,
        r.active_customers,
        (r.active_customers * 100.0 / s.customers_in_cohort) as retention_percent
    FROM retention r
    JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
    ORDER BY r.cohort_month, r.period_number
    """
    return engine.execute_query(query)
