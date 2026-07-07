import pandas as pd
import os

def export_excel(reports: dict, output_path: str):
    """Exports multiple reports (DataFrames) to a single Excel file with multiple sheets."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df in reports.items():
            if df is not None:
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
