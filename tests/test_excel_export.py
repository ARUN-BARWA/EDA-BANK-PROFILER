import pytest
import os
import pandas as pd
from bank_eda_profiler.reports.excel_report import export_excel

def test_excel_export(tmp_path):
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"C": [5, 6]})
    reports = {"report1": df1, "report2": df2, "empty": None}
    
    output_path = os.path.join(tmp_path, "test_export.xlsx")
    export_excel(reports, output_path)
    
    assert os.path.exists(output_path)
    
    # Verify contents
    res1 = pd.read_excel(output_path, sheet_name="report1")
    assert len(res1) == 2
