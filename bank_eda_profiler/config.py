import yaml
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class ReportConfig:
    engine: str = "duckdb"
    privacy_mode: bool = True
    sample_rows: Optional[int] = 100000
    output_dir: str = "reports"
    tables: Dict[str, str] = field(default_factory=dict)
    column_mapping: Dict[str, Dict[str, str]] = field(default_factory=dict)
    
    @classmethod
    def from_yaml(cls, path: str) -> "ReportConfig":
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
            
        return cls(
            engine=data.get("engine", "duckdb"),
            privacy_mode=data.get("privacy_mode", True),
            sample_rows=data.get("sample_rows", 100000),
            output_dir=data.get("output_dir", "reports"),
            tables=data.get("tables", {}),
            column_mapping=data.get("column_mapping", {})
        )
