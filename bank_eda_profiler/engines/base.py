from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseEngine(ABC):
    @abstractmethod
    def load_table(self, name: str, path: str, format: str = "parquet"):
        pass

    @abstractmethod
    def get_row_count(self, name: str) -> int:
        pass

    @abstractmethod
    def get_column_stats(self, name: str, column: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute_query(self, query: str) -> Any:
        pass
