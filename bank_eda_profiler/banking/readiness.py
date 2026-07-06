import json
import os
from jinja2 import Environment, FileSystemLoader
from .report_requirements import REPORT_REQUIREMENTS

class ReadinessReport:
    def __init__(self, report_name: str, status: str, score: float, details: dict = None):
        self.report_name = report_name
        self.status = status
        self.score = score
        self.details = details or {}

    @property
    def is_ready(self) -> bool:
        return self.status == "READY"
        
    @property
    def missing_tables(self) -> list:
        return self.details.get("required_tables_missing", [])
        
    @property
    def missing_fields(self) -> list:
        return self.details.get("required_fields_missing", [])
        
    def to_dict(self) -> dict:
        return {
            "report_name": self.report_name,
            "status": self.status,
            "score": self.score,
            "is_ready": self.is_ready,
            "missing_tables": self.missing_tables,
            "missing_fields": self.missing_fields,
            "details": self.details
        }

    def to_text(self) -> str:
        res = f"{self.report_name.replace('_', ' ').title()} Readiness\n\n"
        res += f"Status: {self.status}\nScore: {self.score}/100\n\n"
        if self.details:
            for k, v in self.details.items():
                if isinstance(v, list):
                    res += f"{k.replace('_', ' ').capitalize()}:\n"
                    for item in v:
                        res += f"- {item}\n"
                else:
                    res += f"{k.replace('_', ' ').capitalize()}:\n- {v}\n"
                res += "\n"
        return res

    def to_json(self) -> str:
        return json.dumps({
            "report_name": self.report_name,
            "status": self.status,
            "score": self.score,
            "details": self.details
        }, indent=2)
        
    def to_html(self) -> str:
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('readiness.html')
        return template.render(report=self)

def check_requirements(report_name: str, available_tables: list, available_schemas: dict) -> ReadinessReport:
    if report_name not in REPORT_REQUIREMENTS:
        return ReadinessReport(report_name, "UNKNOWN", 0, {"error": f"Report '{report_name}' not defined in registry."})
    
    reqs = REPORT_REQUIREMENTS[report_name]
    
    details = {
        "required_tables_missing": [],
        "required_tables_available": [],
        "required_fields_missing": [],
        "required_fields_available": [],
        "optional_fields_missing": [],
        "optional_fields_available": [],
        "fallback_suggestions": []
    }
    
    # Tables
    for t in reqs.get("required_tables", []):
        if t not in available_tables:
            details["required_tables_missing"].append(t)
        else:
            details["required_tables_available"].append(t)
            
    if details["required_tables_missing"]:
        return ReadinessReport(report_name, "NOT_READY", 0, details)
        
    # Fields
    req_fields_total = 0
    req_fields_found = 0
    
    for table, fields in reqs.get("required_fields", {}).items():
        if table in available_schemas:
            schema_cols = available_schemas[table]
            for f in fields:
                req_fields_total += 1
                if f not in schema_cols:
                    details["required_fields_missing"].append(f"{table}.{f}")
                else:
                    details["required_fields_available"].append(f"{table}.{f}")
                    req_fields_found += 1
                    
    for table, fields in reqs.get("optional_fields", {}).items():
        if table in available_schemas:
            schema_cols = available_schemas[table]
            for f in fields:
                if f not in schema_cols:
                    details["optional_fields_missing"].append(f"{table}.{f}")
                else:
                    details["optional_fields_available"].append(f"{table}.{f}")

    # Fallbacks
    for k, v in reqs.get("fallback_rules", {}).items():
        details["fallback_suggestions"].append(f"{k}: {v}")

    if req_fields_total > 0:
        score = (req_fields_found / req_fields_total) * 100
    else:
        score = 100.0
        
    if details["required_fields_missing"]:
        status = "PARTIALLY_READY"
        # cap score at 99 if missing required fields
        score = min(score, 99.0) 
    else:
        status = "READY"
        score = 100.0
        
    return ReadinessReport(report_name, status, round(score, 2), details)
