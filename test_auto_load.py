from bank_eda_profiler.profiler import BankProfiler

print("=== Manual Loading ===")
profiler1 = BankProfiler()
profiler1.load({"leads": "data/lead_master.parquet"})
print("Loaded:", profiler1.config.tables.keys())

print("\n=== Auto Loading (Single File) ===")
profiler2 = BankProfiler()
profiler2.load("data/lead_master.parquet")
print("Loaded:", profiler2.config.tables.keys())

print("\n=== Auto Loading (List of Files) ===")
profiler3 = BankProfiler()
profiler3.load(["data/account_master.parquet", "data/lead_master.parquet"])
print("Loaded:", profiler3.config.tables.keys())
