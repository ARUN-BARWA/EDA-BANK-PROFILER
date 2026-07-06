import os
import json
import pandas as pd
import numpy as np

def is_fg_available():
    try:
        from data_profiling import ProfileReport
        return True
    except ImportError:
        return False

def _generate_fallback_profile(df, table_name, output_dir):
    """
    Generates a generic HTML/JSON profile report using built-in pandas/plotly
    capabilities when fg-data-profiling is not installed.
    """
    report_dir = os.path.join(output_dir, "fg_profiles")
    os.makedirs(report_dir, exist_ok=True)
    
    html_path = os.path.join(report_dir, f"{table_name}_profile.html")
    json_path = os.path.join(report_dir, f"{table_name}_profile.json")

    row_count = len(df)
    col_count = len(df.columns)
    duplicate_count = int(df.duplicated().sum())

    missing = df.isnull().sum().to_dict()
    unique = df.nunique().to_dict()
    types = df.dtypes.astype(str).to_dict()

    warnings = []
    variables = {}

    for col in df.columns:
        col_data = df[col]
        col_missing = int(missing[col])
        col_unique = int(unique[col])
        col_type = types[col]

        var_info = {
            "type": col_type,
            "missing": col_missing,
            "missing_pct": round((col_missing / row_count) * 100, 2) if row_count > 0 else 0,
            "unique": col_unique,
            "unique_pct": round((col_unique / row_count) * 100, 2) if row_count > 0 else 0,
        }

        # Check for warnings
        if col_unique == 1:
            warnings.append(f"{col} is constant (only 1 unique value).")
        if col_unique > 0 and col_unique < row_count:
            top_val_count = col_data.value_counts().iloc[0] if not col_data.dropna().empty else 0
            if top_val_count / row_count > 0.95:
                warnings.append(f"{col} is near-constant (one value > 95%).")
        if col_unique == row_count and row_count > 1:
            warnings.append(f"{col} might be a potential ID (all values unique).")

        # Column-specific summaries
        if pd.api.types.is_numeric_dtype(col_data):
            if col_unique > 10 and not pd.api.types.is_bool_dtype(col_data):
                var_info["mean"] = float(col_data.mean()) if not pd.isna(col_data.mean()) else None
                var_info["std"] = float(col_data.std()) if not pd.isna(col_data.std()) else None
                var_info["min"] = float(col_data.min()) if not pd.isna(col_data.min()) else None
                var_info["25%"] = float(col_data.quantile(0.25)) if not pd.isna(col_data.quantile(0.25)) else None
                var_info["50%"] = float(col_data.quantile(0.50)) if not pd.isna(col_data.quantile(0.50)) else None
                var_info["75%"] = float(col_data.quantile(0.75)) if not pd.isna(col_data.quantile(0.75)) else None
                var_info["max"] = float(col_data.max()) if not pd.isna(col_data.max()) else None
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            var_info["min_date"] = str(col_data.min())
            var_info["max_date"] = str(col_data.max())
        else:
            if col_unique > 100:
                warnings.append(f"{col} has high cardinality ({col_unique} distinct values).")
            # Top values
            val_counts = col_data.value_counts().head(5)
            var_info["top_values"] = val_counts.to_dict()

        variables[col] = var_info

    json_data = {
        "table_name": table_name,
        "row_count": row_count,
        "col_count": col_count,
        "duplicate_count": duplicate_count,
        "variables": variables,
        "warnings": warnings,
        "is_fallback": True
    }

    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=4, default=str)

    html_content = f"""
    <html>
    <head><title>Data Profiling Report - {table_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .warning-banner {{ background-color: #fff3cd; color: #856404; padding: 15px; margin-bottom: 20px; border-left: 5px solid #ffeeba; }}
        h1, h2, h3 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .warnings ul {{ color: #d9534f; }}
    </style>
    </head>
    <body>
        <div class="warning-banner">
            <strong>Notice:</strong> fg-data-profiling is not installed. This report was generated using Bank EDA Profiler's built-in DuckDB/Polars fallback profiler. Install <code>bank_eda_profiler[fg]</code> for full fg-data-profiling reports.
        </div>
        <h1>Data Profiling Report - {table_name}</h1>
        <h2>Overview</h2>
        <table>
            <tr><th>Rows</th><td>{row_count}</td></tr>
            <tr><th>Columns</th><td>{col_count}</td></tr>
            <tr><th>Duplicates</th><td>{duplicate_count}</td></tr>
        </table>
        
        <h2>Alerts / Warnings</h2>
        <div class="warnings">
            <ul>
                {''.join([f"<li>{w}</li>" for w in warnings])}
            </ul>
        </div>
        
        <h2>Variables</h2>
    """

    for col, info in variables.items():
        html_content += f"<h3>{col}</h3>"
        html_content += "<table>"
        for k, v in info.items():
            if k == "top_values":
                html_content += f"<tr><th>Top Values</th><td><pre>{json.dumps(v, indent=2)}</pre></td></tr>"
            else:
                html_content += f"<tr><th>{k.capitalize()}</th><td>{v}</td></tr>"
        html_content += "</table>"

    html_content += """
    </body>
    </html>
    """

    with open(html_path, 'w') as f:
        f.write(html_content)

    return {
        "html_path": html_path,
        "json_path": json_path,
        "sample_size": row_count,
        "type": "fallback"
    }


def generate_fg_or_fallback_profile(
    engine,
    table_name: str,
    output_dir: str,
    sample_rows: int = 100000,
    minimal: bool = True,
    explorative: bool = True,
    allow_full_profile: bool = False
):
    """
    Generates an HTML and JSON profile report for a given table.
    Uses fg-data-profiling if available, otherwise falls back to generic profiler.
    Safely samples the table using the SQL engine before converting to Pandas.
    """
    # Sample data efficiently using DuckDB/Polars
    if allow_full_profile and sample_rows <= 0:
        query = f"SELECT * FROM {table_name}"
    else:
        actual_sample_rows = sample_rows if sample_rows > 0 else 100000
        query = f"SELECT * FROM {table_name} LIMIT {actual_sample_rows}"
    
    # Execute and convert to pandas
    df = engine.execute(query).df()
    
    if df.empty:
        return None
        
    if is_fg_available():
        from data_profiling import ProfileReport
        
        profile = ProfileReport(df, title=f"Data Profiling Report - {table_name}", minimal=minimal, explorative=explorative)
        
        report_dir = os.path.join(output_dir, "fg_profiles")
        os.makedirs(report_dir, exist_ok=True)
        
        html_path = os.path.join(report_dir, f"{table_name}_profile.html")
        json_path = os.path.join(report_dir, f"{table_name}_profile.json")
        
        profile.to_file(html_path)
        profile.to_file(json_path)
        
        return {
            "html_path": html_path,
            "json_path": json_path,
            "sample_size": len(df),
            "type": "fg-data-profiling"
        }
    else:
        return _generate_fallback_profile(df, table_name, output_dir)
