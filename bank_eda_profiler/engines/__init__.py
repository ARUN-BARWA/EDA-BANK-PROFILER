from .base import BaseEngine
from .duckdb_engine import DuckDBEngine
from .polars_engine import PolarsEngine
from .pandas_engine import PandasEngine

def get_engine(name: str) -> BaseEngine:
    name = name.lower()
    if name == "duckdb":
        return DuckDBEngine()
    elif name == "polars":
        return PolarsEngine()
    elif name == "pandas":
        return PandasEngine()
    else:
        raise ValueError(f"Unknown engine: {name}")
