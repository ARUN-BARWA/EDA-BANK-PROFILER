from ..engines import BaseEngine
from typing import Any

def generate_campaign_performance(engine: BaseEngine, campaign_table: str) -> Any:
    query = f"""
    SELECT 
        campaign_id,
        campaign_name,
        channel,
        target_region,
        campaign_cost,
        impressions,
        clicks,
        leads_generated,
        applications_started,
        accounts_opened,
        funded_accounts
    FROM {campaign_table}
    """
    df = engine.execute_query(query)
    
    if not df.empty:
        df["click_through_rate"] = (df["clicks"] / df["impressions"]) * 100
        df["lead_to_account_conversion_percent"] = (df["accounts_opened"] / df["leads_generated"]) * 100
        df["cost_per_lead"] = df["campaign_cost"] / df["leads_generated"]
        df["cost_per_account"] = df["campaign_cost"] / df["accounts_opened"]
        df["cost_per_funded_account"] = df["campaign_cost"] / df["funded_accounts"]
        df["funded_account_quality_percent"] = (df["funded_accounts"] / df["accounts_opened"]) * 100
        
        df.replace([float('inf'), -float('inf')], 0, inplace=True)
        df.fillna(0, inplace=True)
        df = df.round(2)
        
    return df
