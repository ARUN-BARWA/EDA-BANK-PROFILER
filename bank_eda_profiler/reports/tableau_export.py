import os
import json

def export_tableau(reports: dict, output_dir: str):
    """Exports reports as CSV files for Tableau consumption."""
    tab_dir = os.path.join(output_dir, "tableau")
    os.makedirs(tab_dir, exist_ok=True)
    
    for name, df in reports.items():
        if df is not None:
            df.to_csv(os.path.join(tab_dir, f"{name}.csv"), index=False)
            
    # Metadata
    with open(os.path.join(tab_dir, "data_dictionary.json"), 'w') as f:
        json.dump({"reports": list(reports.keys())}, f)
