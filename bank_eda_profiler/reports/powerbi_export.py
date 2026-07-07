import os
import json

def export_powerbi(reports: dict, output_dir: str):
    """Exports reports as Parquet files for PowerBI consumption."""
    pbi_dir = os.path.join(output_dir, "powerbi")
    os.makedirs(pbi_dir, exist_ok=True)
    
    for name, df in reports.items():
        if df is not None:
            df.to_parquet(os.path.join(pbi_dir, f"{name}.parquet"), index=False)
            
    # Metadata
    with open(os.path.join(pbi_dir, "data_dictionary.json"), 'w') as f:
        json.dump({"reports": list(reports.keys())}, f)
