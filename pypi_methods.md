# Using Bank EDA Profiler in Python

Once you have installed the package via pip:
```bash
pip install bank-eda-profiler
```
You can import its methods directly into your Python scripts or Jupyter Notebooks. The core of the library revolves around the `BankProfiler` and `ReportConfig` classes.

This guide demonstrates how to use the profiler whether you have just one dataset or multiple interlinked banking datasets.

---

## Example 1: Profiling a Single File

You don't need a massive data warehouse to use this tool! If you just have a single flat file (like an account dump or lead tracker), you can profile it on its own.

```python
from bank_eda_profiler.profiler import BankProfiler
from bank_eda_profiler.config import ReportConfig

# 1. Define your data source
# The dictionary key ("accounts") tells the profiler what type of banking data this is.
data_sources = {
    "accounts": "path/to/your/account_data.csv"
}

# 2. Setup your configuration and column mapping
# Since your CSV columns might not match our standard names exactly, you map them here.
config = ReportConfig(
    engine="duckdb",                      # 'duckdb' or 'polars'
    output_dir="single_file_reports",     # Where the dashboard HTML will be saved
    column_mapping={
        "accounts": {
            "account_id": "Acc_No",       # Mapping our standard 'account_id' to your 'Acc_No'
            "open_date": "Date_Opened",
            "balance": "Current_Balance"
        }
    }
)

# 3. Initialize the Profiler
profiler = BankProfiler(data_sources=data_sources, config=config)

# 4. Use Profiler Methods
# Check what reports the library can generate with your specific columns
readiness = profiler.analyze_dataset_readiness()
print("Readiness Scores:", readiness)

# Ask the profiler which reports passed the readiness check
available = profiler.discover_available_reports()
print("Reports that can be built:", available)

# Generate the interactive HTML dashboard!
profiler.generate_possible_reports()
profiler.generate_html_dashboard()
print("Reports generated successfully!")
```

---

## Example 2: Profiling Multiple Interlinked Files

The true power of the `BankProfiler` unlocks when you provide multiple files (e.g. leads, applications, accounts, and transactions). The library will automatically join them to generate rich insights like Conversion Funnels and Cohort Retention.

```python
from bank_eda_profiler.profiler import BankProfiler
from bank_eda_profiler.config import ReportConfig

# 1. Define multiple data sources
# Keys must correspond to supported logical tables (e.g., 'leads', 'applications', 'accounts')
data_sources = {
    "leads": "path/to/lead_data.parquet",
    "applications": "path/to/application_data.parquet",
    "accounts": "path/to/account_data.csv",
    "transactions": "path/to/transaction_history.csv"
}

# 2. Setup global configurations and mappings for all files
config = ReportConfig(
    engine="duckdb",
    output_dir="multi_file_reports",
    privacy_mode=True,         # Auto-masks PII in the generated dashboard
    sample_rows=500000,        # Sample data if files are too large
    column_mapping={
        "leads": {
            "lead_id": "LeadID",
            "created_at": "Lead_Date"
        },
        "applications": {
            "application_id": "AppID",
            "lead_id": "LeadID",
            "status": "App_Status"
        },
        "accounts": {
            "account_id": "AccID",
            "customer_id": "CustID",
            "open_date": "Opened_On"
        }
        # You don't have to map every file if their columns already match exactly!
    }
)

# 3. Initialize the Profiler
profiler = BankProfiler(data_sources=data_sources, config=config)

# 4. Let the Profiler help you!
# If you forgot to map a column, the profiler can use AI inference to suggest mappings
suggestions = profiler.suggest_column_mappings()
if suggestions:
    print("Consider adding these mappings to your config:")
    print(suggestions)

# 5. Generate the ultimate multi-table banking dashboard
profiler.generate_possible_reports()
profiler.generate_html_dashboard()
print("Comprehensive Banking Dashboard created!")
```

### Key Takeaway
Whether you provide 1 file or 12 files, the library dynamically adapts. The `BankProfiler` figures out exactly which insights (out of dozens of possible banking KPIs) can be securely and accurately calculated from the data you provide.
