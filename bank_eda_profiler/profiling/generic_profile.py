from ..engines import BaseEngine
from typing import Dict, Any

def generate_profile(engine: BaseEngine, table: str) -> Dict[str, Any]:
    row_count = engine.get_row_count(table)
    
    # Simple query to get some column names to profile
    df_desc = engine.execute_query(f"DESCRIBE {table}")
    cols = df_desc['column_name'].tolist()
    
    col_stats = []
    
    # We only take the first 5 columns to speed up profiling for now
    for col in cols[:5]:
        stats = engine.get_column_stats(table, col)
        col_stats.append({
            "column": col,
            "count": stats["count"],
            "unique": stats["unique"],
            "missing": stats["missing"]
        })
        
    return {
        "table_name": table,
        "row_count": row_count,
        "column_stats": col_stats
    }
