from typing import Dict, Any, Optional
import os
import pandas as pd
from .config import ReportConfig
from .engines import get_engine
from .io.readers import load_data
from .io.schema_inference import infer_schema
from .io.column_mapping import suggest_column_mappings
from .profiling.generic_profile import generate_profile
from .profiling.privacy_scan import scan_for_pii
from .profiling.fg_profile import generate_fg_or_fallback_profile

from .banking.readiness import check_requirements
from .banking.activation import generate_activation_quality
from .banking.regional_mis import generate_regional_mis
from .banking.kyc import generate_kyc_dropoff
from .banking.sales_productivity import generate_sales_productivity
from .banking.dormancy import generate_dormancy_report
from .banking.campaign import generate_campaign_performance
from .banking.funnel import generate_funnel
from .banking.cohort import generate_cohort
from .banking.segmentation import generate_segmentation
from .banking.report_requirements import REPORT_REQUIREMENTS

from .reports.html_report import generate_html_reports
from .reports.excel_report import export_excel
from .reports.powerbi_export import export_powerbi
from .reports.tableau_export import export_tableau

class BankProfiler:
    def __init__(self, data_sources: Optional[Dict[str, str]] = None, config: Optional[ReportConfig] = None):
        self.config = config or ReportConfig()
        if data_sources:
            self.config.tables.update(data_sources)
            
        self.engine = get_engine(self.config.engine)
        load_data(self.engine, self.config.tables)
        
        self.schemas = {}
        for table in self.config.tables.keys():
            self.schemas[table] = list(infer_schema(self.engine, table).keys())
            
        self.generated_reports = {}

    @classmethod
    def from_config(cls, path: str) -> "BankProfiler":
        config = ReportConfig.from_yaml(path)
        return cls(config=config)
        
    def _apply_mapping(self, table: str, col: str) -> str:
        """Returns the actual column name based on yaml config mapping."""
        if table in self.config.column_mapping:
            for logical, physical in self.config.column_mapping[table].items():
                if logical == col:
                    return physical
        return col
        
    def suggest_column_mappings(self, report_type: Optional[str] = None) -> Dict[str, str]:
        all_suggestions = {}
        if report_type:
            if report_type not in REPORT_REQUIREMENTS:
                return {}
            reqs = REPORT_REQUIREMENTS[report_type]
            for table, fields in reqs.get("required_fields", {}).items():
                if table in self.schemas:
                    all_suggestions.update(suggest_column_mappings(self.schemas[table], fields))
        else:
            for rep, reqs in REPORT_REQUIREMENTS.items():
                for table, fields in reqs.get("required_fields", {}).items():
                    if table in self.schemas:
                        all_suggestions.update(suggest_column_mappings(self.schemas[table], fields))
        return all_suggestions
        
    def discover_available_reports(self):
        available = []
        for report_name in REPORT_REQUIREMENTS.keys():
            readiness = self.check_requirements(report_name)
            if readiness.is_ready:
                available.append(report_name)
        return available

    def analyze_dataset_readiness(self):
        readiness_dict = {}
        for report_name in REPORT_REQUIREMENTS.keys():
            readiness_dict[report_name] = self.check_requirements(report_name).to_dict()
        return readiness_dict

    def generate_possible_reports(self):
        possible = self.discover_available_reports()
        for rep in possible:
            self.generate_report(rep)
        return possible

    def generate_report(self, report_name: str):
        mapping = {
            "daily_sales_dashboard": self.generate_daily_sales_dashboard,
            "kyc_dropoff_report": self.generate_kyc_dropoff_report,
            "activation_quality_report": self.generate_activation_quality_report,
            "salesperson_productivity_report": self.generate_salesperson_productivity_report,
            "dormancy_report": self.generate_dormancy_report,
            "campaign_performance_report": self.generate_campaign_performance_report,
            "funnel_analysis": self.generate_funnel_analysis,
            "cohort_analysis": self.generate_cohort_analysis,
            "customer_segmentation": self.generate_customer_segmentation
        }
        if report_name in mapping:
            mapping[report_name]()

    def profile_table(self, table_name: str):
        if table_name not in self.schemas:
            return None
        prof = generate_profile(self.engine, table_name)
        return prof

    def profile_dataset(self, path: str):
        # Infer table name from path
        table_name = os.path.splitext(os.path.basename(path))[0]
        self.config.tables[table_name] = path
        load_data(self.engine, {table_name: path})
        self.schemas[table_name] = list(infer_schema(self.engine, table_name).keys())
        return self.profile_table(table_name)

    def explain_missing_fields(self, report_name: str):
        readiness = self.check_requirements(report_name)
        explanation = f"Readiness for {report_name}: {readiness.score}%\n"
        explanation += f"Ready: {readiness.is_ready}\n"
        if not readiness.is_ready:
            explanation += f"Missing tables: {readiness.missing_tables}\n"
            explanation += f"Missing fields: {readiness.missing_fields}\n"
        reqs = REPORT_REQUIREMENTS.get(report_name, {})
        if "fallback_rules" in reqs:
            explanation += f"Fallback logic: {reqs['fallback_rules']}\n"
        return explanation

    def generate_fg_profile(self, table_name: str, sample_rows: int = 100000, minimal: bool = True, explorative: bool = True, allow_full_profile: bool = False):
        if table_name not in self.schemas:
            return None
        return generate_fg_or_fallback_profile(
            self.engine,
            table_name,
            self.config.output_dir,
            sample_rows,
            minimal,
            explorative,
            allow_full_profile
        )

    def generate_fg_profile_all(self, sample_rows: int = 100000, minimal: bool = True, explorative: bool = True, allow_full_profile: bool = False):
        results = {}
        for table in self.schemas.keys():
            results[table] = self.generate_fg_profile(table, sample_rows, minimal, explorative, allow_full_profile)
        return results

    def profile_all(self):
        profiles = []
        privacy_warnings = {}
        for table, cols in self.schemas.items():
            prof = generate_profile(self.engine, table)
            profiles.append(prof)
            if self.config.privacy_mode:
                warnings = scan_for_pii(cols)
                if warnings:
                    privacy_warnings[table] = warnings
                    
        self.generated_reports["profiles"] = pd.DataFrame(profiles)
        if privacy_warnings:
            # Flatten privacy warnings for export
            flat_warns = []
            for t, ws in privacy_warnings.items():
                for c, w in ws.items():
                    flat_warns.append({"table": t, "column": c, "warning": w})
            self.generated_reports["privacy_warnings"] = pd.DataFrame(flat_warns)

    def check_requirements(self, report_name: str):
        available_tables = list(self.config.tables.keys())
        mapped_schemas = {}
        # we check requirements against logic names, so we pretend schemas have them if mapped
        for table, cols in self.schemas.items():
            mapped_cols = list(cols)
            if table in self.config.column_mapping:
                for logical, physical in self.config.column_mapping[table].items():
                    if physical in mapped_cols:
                        mapped_cols.append(logical)
            mapped_schemas[table] = mapped_cols
            
        readiness = check_requirements(report_name, available_tables, mapped_schemas)
        
        # export readiness report
        os.makedirs(self.config.output_dir, exist_ok=True)
        with open(os.path.join(self.config.output_dir, f"{report_name}_readiness.json"), 'w') as f:
            f.write(readiness.to_json())
            
        with open(os.path.join(self.config.output_dir, f"{report_name}_readiness.html"), 'w') as f:
            f.write(readiness.to_html())
            
        return readiness

    def generate_daily_sales_dashboard(self):
        if "leads" in self.config.tables and "accounts" in self.config.tables:
            df = generate_regional_mis(self.engine, "leads", "accounts")
            self.generated_reports["daily_sales"] = df

    def generate_kyc_dropoff_report(self):
        if "applications" in self.config.tables and "vkyc" in self.config.tables:
            df = generate_kyc_dropoff(self.engine, "applications", "vkyc")
            self.generated_reports["kyc_dropoff"] = df

    def generate_activation_quality_report(self):
        if "accounts" in self.config.tables:
            df = generate_activation_quality(self.engine, "accounts")
            self.generated_reports["activation_quality"] = df

    def generate_salesperson_productivity_report(self):
        if "sales" in self.config.tables and "targets" in self.config.tables:
            df = generate_sales_productivity(self.engine, "sales", "targets")
            self.generated_reports["sales_productivity"] = df

    def generate_dormancy_report(self):
        if "accounts" in self.config.tables:
            df = generate_dormancy_report(self.engine, "accounts")
            self.generated_reports["dormancy"] = df

    def generate_campaign_performance_report(self):
        if "campaigns" in self.config.tables:
            df = generate_campaign_performance(self.engine, "campaigns")
            self.generated_reports["campaign_performance"] = df

    def generate_funnel_analysis(self):
        if "applications" in self.config.tables:
            steps = ["application_start_time", "otp_verified_flag", "pan_verified_flag", "vkyc_completed_time", "account_opened_flag"]
            df = generate_funnel(self.engine, "applications", steps)
            self.generated_reports["funnel_analysis"] = df

    def generate_cohort_analysis(self):
        if "accounts" in self.config.tables and "transactions" in self.config.tables:
            df = generate_cohort(self.engine, "accounts", "account_open_date", "first_transaction_date")
            self.generated_reports["cohort_analysis"] = df

    def generate_customer_segmentation(self):
        if "accounts" in self.config.tables:
            df = generate_segmentation(self.engine, "accounts")
            self.generated_reports["segmentation"] = df

    def generate_html_dashboard(self):
        generate_html_reports(self.generated_reports, self.config.output_dir)

    def export_excel(self):
        path = os.path.join(self.config.output_dir, "bank_reports.xlsx")
        export_excel(self.generated_reports, path)

    def export_bi_ready_files(self):
        export_powerbi(self.generated_reports, self.config.output_dir)
        export_tableau(self.generated_reports, self.config.output_dir)
