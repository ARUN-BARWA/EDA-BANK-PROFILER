import duckdb
from typing import Any, Dict
from .base import BaseEngine

class DuckDBEngine(BaseEngine):
    def __init__(self):
        self.con = duckdb.connect(database=':memory:')

    def load_table(self, name: str, path: str, format: str = "parquet"):
        if format == "parquet":
            self.con.execute(f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_parquet('{path}')")
        elif format == "csv":
            self.con.execute(f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_csv_auto('{path}')")
        else:
            raise ValueError(f"Unsupported format {format} for DuckDBEngine")

    def get_row_count(self, name: str) -> int:
        result = self.con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()
        return result[0] if result else 0

    def get_column_stats(self, name: str, column: str) -> Dict[str, Any]:
        result = self.con.execute(f"""
            SELECT 
                COUNT({column}) as count, 
                COUNT(DISTINCT {column}) as unique_count,
                SUM(CASE WHEN {column} IS NULL THEN 1 ELSE 0 END) as missing_count
            FROM {name}
        """).fetchone()
        return {
            "count": result[0],
            "unique": result[1],
            "missing": result[2]
        }

    def execute_query(self, query: str) -> Any:
        return self.con.execute(query).df()
