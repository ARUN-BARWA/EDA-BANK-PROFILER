import polars as pl
from typing import Any, Dict
from .base import BaseEngine

class PolarsEngine(BaseEngine):
    def __init__(self):
        self.tables = {}

    def load_table(self, name: str, path: str, format: str = "parquet"):
        if format == "parquet":
            self.tables[name] = pl.scan_parquet(path)
        elif format == "csv":
            self.tables[name] = pl.scan_csv(path)
        else:
            raise ValueError(f"Unsupported format {format} for PolarsEngine")

    def get_row_count(self, name: str) -> int:
        df = self.tables[name].select(pl.count()).collect()
        return df.item()

    def get_column_stats(self, name: str, column: str) -> Dict[str, Any]:
        df = self.tables[name].select([
            pl.col(column).count().alias("count"),
            pl.col(column).n_unique().alias("unique"),
            pl.col(column).null_count().alias("missing")
        ]).collect()
        
        return {
            "count": df["count"][0],
            "unique": df["unique"][0],
            "missing": df["missing"][0]
        }

    def execute_query(self, query: str) -> Any:
        raise NotImplementedError("SQL queries not natively supported in PolarsEngine without SQLContext")
