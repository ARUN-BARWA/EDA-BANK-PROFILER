import pandas as pd
from typing import Any, Dict
from .base import BaseEngine

class PandasEngine(BaseEngine):
    def __init__(self):
        self.tables = {}

    def load_table(self, name: str, path: str, format: str = "parquet"):
        if format == "parquet":
            self.tables[name] = pd.read_parquet(path)
        elif format == "csv":
            self.tables[name] = pd.read_csv(path)
        else:
            raise ValueError(f"Unsupported format {format} for PandasEngine")

    def get_row_count(self, name: str) -> int:
        return len(self.tables[name])

    def get_column_stats(self, name: str, column: str) -> Dict[str, Any]:
        df = self.tables[name]
        return {
            "count": int(df[column].count()),
            "unique": int(df[column].nunique()),
            "missing": int(df[column].isnull().sum())
        }

    def execute_query(self, query: str) -> Any:
        raise NotImplementedError("PandasEngine does not support SQL queries directly.")
