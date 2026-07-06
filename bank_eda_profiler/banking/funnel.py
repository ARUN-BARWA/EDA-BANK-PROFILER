from typing import List, Dict, Any
from ..engines import BaseEngine

def generate_funnel(engine: BaseEngine, table: str, steps: List[str], group_by: List[str] = None) -> Any:
    # Build standard funnel logic
    
    selects = []
    for s in steps:
        if s == "otp_verified_flag" or s == "pan_verified_flag" or s == "account_opened_flag":
            selects.append(f"SUM(CASE WHEN {s} = True THEN 1 ELSE 0 END) as {s}_count")
        else:
            selects.append(f"SUM(CASE WHEN {s} IS NOT NULL THEN 1 ELSE 0 END) as {s}_count")
            
    if group_by:
        group_cols = ", ".join(group_by)
        query = f"SELECT {group_cols}, {', '.join(selects)} FROM {table} GROUP BY {group_cols}"
    else:
        query = f"SELECT {', '.join(selects)} FROM {table}"
        
    df = engine.execute_query(query)
    
    # We transpose it to show a real funnel view (step_name, users_at_step)
    # Pandas transformation for simplicity of output formatting
    import pandas as pd
    
    funnel_data = []
    if not df.empty:
        row = df.iloc[0]
        first_step_val = row[f"{steps[0]}_count"]
        prev_step_val = first_step_val
        
        for i, s in enumerate(steps):
            val = row[f"{s}_count"]
            drop_count = prev_step_val - val
            drop_pct = (drop_count / prev_step_val * 100) if prev_step_val > 0 else 0
            conv_prev = (val / prev_step_val * 100) if prev_step_val > 0 else 0
            conv_first = (val / first_step_val * 100) if first_step_val > 0 else 0
            
            funnel_data.append({
                "step_name": s,
                "users_at_step": val,
                "drop_count": drop_count,
                "drop_percent": round(drop_pct, 2),
                "conversion_from_previous": round(conv_prev, 2),
                "conversion_from_first": round(conv_first, 2)
            })
            prev_step_val = val
            
    return pd.DataFrame(funnel_data)
