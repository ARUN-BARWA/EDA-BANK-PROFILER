from ..engines import BaseEngine
from typing import Dict, Any

def infer_schema(engine: BaseEngine, table_name: str) -> Dict[str, str]:
    """Infers schema for a given table using the engine."""
    # Assuming duckdb is the underlying engine for schema inference right now
    # We would run a query to get column types
    try:
        df = engine.execute_query(f"DESCRIBE {table_name}")
        schema = dict(zip(df['column_name'], df['column_type']))
        return schema
    except NotImplementedError:
        # Fallback for pandas/polars
        pass
    except Exception as e:
        print(f"Schema inference failed for {table_name}: {e}")
        
    return {}
