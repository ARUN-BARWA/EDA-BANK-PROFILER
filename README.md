# Bank EDA Profiler 🏦📊

> **A scalable Python library for profiling, validating, and reporting on banking, digital-sales, and customer portfolio datasets.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## 📖 What it does
`bank_eda_profiler` is a specialized analytical tool built specifically for the financial domain. It performs high-speed Exploratory Data Analysis (EDA), validates the shape of your data against standard banking models, and automatically generates business-critical MIS (Management Information System) reports like Activation Quality, KYC Drop-offs, Sales Productivity, and Dormancy tracking.

## ❓ Why it exists
Banking and financial datasets are often massive, highly fragmented, and subject to strict privacy regulations. Generic EDA tools (like standard pandas profiling) often run out of memory (OOM) on large transaction datasets and don't understand banking-specific logic (like funnels, cohorts, or account structures). This library solves that by bringing scalability, privacy-awareness, and domain-specific KPIs into one box.

## 🎯 Who is it for?
- **Data Analysts & Scientists** working in banks, fintechs, or lending institutions.
- **Business Intelligence (BI) Engineers** looking to accelerate data prep for Tableau/Power BI.
- **Product Managers** who need to quickly understand funnels and feature drop-offs.
- **Open-Source Contributors** interested in financial modeling and scalable data engineering.

---

## ✨ Key Features

- **Blazing Fast Scalability**: Combines **DuckDB** and **Polars** for out-of-core, large-scale data processing. Say goodbye to Pandas memory errors.
- **Built-in Scalable Profiling**: Generates summary statistics and profiles millions of rows seamlessly.
- **Optional `fg-data-profiling`**: Seamlessly integrates with [fg-data-profiling](https://github.com/data-profiling) for rich, interactive HTML reports via safe sampling.
- **Report Readiness Checks & Validation**: Automatically inspects your data to determine exactly which banking reports can be generated and explains any missing fields.
- **Intelligent Column Mapping**: Suggests how to map your custom, generic columns (e.g., `amt`) to the standard banking model (e.g., `avg_monthly_balance`).
- **Rich Exports**: Generates HTML Dashboards, multi-sheet Excel Reports, and BI-ready Parquet/CSV files (optimized for Power BI and Tableau).
- **Synthetic Data Generation**: Includes a demo generator to create interconnected fake banking datasets for testing and learning.

---

## 🏗️ Architecture Overview

You can provide data to the library in three ways:
1. **A single flat dataset** (e.g., one massive `train.csv` containing everything).
2. **Multiple related datasets** (e.g., `accounts.parquet`, `transactions.parquet`, `leads.csv`).
3. **Synthetic demo datasets** (generated automatically by the library for testing).

The engine parses the data using **DuckDB**, infers the schema, runs a privacy scan, checks readiness against standard banking reporting requirements, and finally runs custom SQL/Polars transformations to yield actionable reports.

---

## 🚀 Installation

### Installation from PyPI
Install the core library (uses DuckDB and Polars):
```bash
pip install bank-eda-profiler
```

### Optional fg-data-profiling support
Install with `fg-data-profiling` support for rich, interactive HTML reports:
```bash
pip install "bank-eda-profiler[fg]"
```

### Development install from GitHub
If you want to contribute or build from source:
```bash
git clone https://github.com/<your-username>/bank-eda-profiler.git
cd bank-eda-profiler
pip install -e ".[dev]"
```

---

## ⚡ Quickstart

### 1. Synthetic Demo Workflow
Don't have data yet? Generate some synthetic data to see the library in action!
```bash
# Generates interconnected synthetic leads, accounts, transactions, etc.
bank-eda generate-demo-data --output ./demo_data
bank-eda dashboard --config config/report_config.yaml
```

### 2. Bring Your Own Data (BYOD) Workflow
Have your own dataset? Here is the best way to get started using Python.

Create a file named `example_run.py`:

```python
from bank_eda_profiler.profiler import BankProfiler
from bank_eda_profiler.config import ReportConfig

# Map your dataset
data_sources = {
    "accounts": "path/to/your/flat_dataset.csv",
    "leads": "path/to/your/flat_dataset.csv" 
    # Add other logical tables pointing to your files as needed
}

# Apply mappings if your columns don't match the standard banking model
config = ReportConfig(
    output_dir="my_reports",
    column_mapping={
        "accounts": {
            "account_id": "Acct_No",
            "account_open_date": "Opened_On"
        }
    }
)

profiler = BankProfiler(data_sources=data_sources, config=config)

# Check what reports are possible
readiness = profiler.analyze_dataset_readiness()
print(readiness)

# Generate a beautiful HTML dashboard of all possible reports
profiler.generate_possible_reports()
profiler.generate_html_dashboard()
```
Run it:
```bash
python example_run.py
```

---

## 💻 CLI Usage

The suite can also be run entirely via the CLI using a `config.yaml` file (see `config/report_config.example.yaml`).

```bash
# Check dataset readiness and explain missing fields
bank-eda inspect --config config/report_config.yaml

# Suggest column mappings for your custom data
bank-eda suggest-mappings --config config/report_config.yaml

# Discover which reports can be generated
bank-eda discover-reports --config config/report_config.yaml

# Generate an HTML Dashboard for all ready reports
bank-eda dashboard --config config/report_config.yaml --type all

# Export to Excel
bank-eda export-excel --config config/report_config.yaml
```

---

## 📊 Supported Banking Reports

Depending on what fields you provide, the library can dynamically generate:

- **Activation Quality Report** (Requires account and funding data)
- **KYC Drop-off Report** (Requires application funnel and VKYC session data)
- **Salesperson Productivity Report** (Requires sales hierarchy, leads, and targets)
- **Dormancy Tracking Report** (Requires accounts and transactions)
- **Campaign Performance Report** (Requires campaign master and attribution)
- **Funnel Analysis** (Step-by-step application drop-offs)
- **Cohort Analysis** (Account opening vs first transaction cohorts)
- **Customer Segmentation** (Demographic and product holding splits)

---

## 🛠 Report Readiness Checker

If you are missing data for a specific report, the library will not crash. Instead, the **Readiness Checker** will:
1. Score your dataset's readiness (e.g., `45% Ready`).
2. Mark the report as `NOT_READY` or `PARTIALLY_READY`.
3. Give you exact instructions on what fields/tables are missing.
4. Suggest column mappings if it detects similar column names in your dataset!

---

## 📂 Formats & BI Exports

### Supported Input Formats
- CSV (`.csv`)
- Parquet (`.parquet`)
- Excel (`.xlsx`)
- SQL / Database Connections (via DuckDB integrations)

### Supported Output Formats
- **HTML Dashboards** (Standalone, shareable via browser)
- **Excel Workbooks** (Multi-sheet summaries for finance/ops teams)
- **JSON** (For programmatic ingestion)

### BI Export Clarification (Power BI / Tableau)
```bash
bank-eda export-bi --config config/report_config.yaml
```
*Note: The library exports highly aggregated, cleaned, and joined **BI-ready Parquet/CSV files**. It does not generate proprietary binary visualization files (like `.pbix` or `.twbx`). You simply import the generated BI-ready files into Power BI Desktop or Tableau to build your visualizations effortlessly.*

---

## 📸 Example Screenshots
*(Note to contributors: Add screenshots of the HTML Dashboard, Readiness Report, and Terminal CLI output here)*
- [Placeholder: HTML Dashboard Screenshot]
- [Placeholder: CLI Inspection Output]

---

## 🤝 Contributing

We love open-source contributors! Whether it's adding a new banking report, optimizing a Polars query, or fixing a bug, your help is welcome.

Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to set up your development environment, run tests, and submit Pull Requests.

---

## 🔐 Maintainer Notes: PyPI Release Process

This repository is configured with **PyPI Trusted Publishing** via GitHub Actions.

If you are the repository owner, you must configure your PyPI account before the automated `.github/workflows/publish.yml` will work:
1. Go to PyPI > Manage Project > Publishing.
2. Add a new Trusted Publisher with:
   - **PyPI Project Name**: `bank-eda-profiler`
   - **GitHub Owner**: `<your-username>`
   - **GitHub Repository**: `bank-eda-profiler`
   - **Workflow Name**: `publish.yml`

*Do not store long-lived PyPI API tokens in GitHub Secrets.* Once configured, simply creating a **GitHub Release** will automatically trigger the workflow to build and securely publish the `.whl` and `.tar.gz` to PyPI.

---

## 🗺️ Roadmap

- [ ] Support for Credit Card specific portfolio reporting (Delinquency roll-rates).
- [ ] Direct database connectors for Snowflake and BigQuery.
- [ ] Integration with Great Expectations for data quality assertions.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer
*This library is an analytical tool and does not provide financial or regulatory advice. Always ensure your data pipelines comply with your local data privacy laws (GDPR, CCPA, etc.) before processing PII (Personally Identifiable Information).*
