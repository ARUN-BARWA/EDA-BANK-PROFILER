from ..engines import BaseEngine
import os

def load_data(engine: BaseEngine, tables_config: dict):
    for table_name, file_path in tables_config.items():
        if os.path.exists(file_path):
            ext = file_path.split('.')[-1]
            engine.load_table(table_name, file_path, format=ext)
        else:
            print(f"Warning: File {file_path} for table {table_name} does not exist.")
