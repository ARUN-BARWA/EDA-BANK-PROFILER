from ..engines import BaseEngine
from typing import Any

def generate_kyc_dropoff(engine: BaseEngine, applications_table: str, vkyc_table: str) -> Any:
    query = f"""
    WITH app_stats AS (
        SELECT 
            a.region,
            a.application_id,
            a.vkyc_required_flag,
            a.account_opened_flag,
            v.status as vkyc_status,
            v.failure_reason as vkyc_failure_reason
        FROM {applications_table} a
        LEFT JOIN {vkyc_table} v ON a.application_id = v.application_id
    )
    SELECT 
        region,
        COUNT(application_id) as applications_started,
        SUM(CASE WHEN vkyc_required_flag = True THEN 1 ELSE 0 END) as vkyc_required,
        SUM(CASE WHEN vkyc_required_flag = True AND vkyc_status = 'COMPLETED' THEN 1 ELSE 0 END) as vkyc_completed,
        SUM(CASE WHEN vkyc_required_flag = True AND vkyc_status IS NULL THEN 1 ELSE 0 END) as vkyc_pending,
        SUM(CASE WHEN vkyc_required_flag = True AND vkyc_status = 'FAILED' THEN 1 ELSE 0 END) as vkyc_failed,
        SUM(CASE WHEN account_opened_flag = True THEN 1 ELSE 0 END) as account_opened
    FROM app_stats
    GROUP BY region
    """
    df = engine.execute_query(query)
    
    if not df.empty:
        df["kyc_to_account_conversion_percent"] = (df["account_opened"] / df["vkyc_completed"]) * 100
        df.replace([float('inf'), -float('inf')], 0, inplace=True)
        df.fillna(0, inplace=True)
        df = df.round(2)
        
    return df
