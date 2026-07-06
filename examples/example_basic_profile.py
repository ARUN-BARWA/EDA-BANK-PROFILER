from bank_eda_profiler import BankProfiler

profiler = BankProfiler.from_config("config/report_config.yaml")

print("Checking Requirements for Activation Quality Report:")
readiness = profiler.check_requirements("activation_quality_report")
print(readiness.to_text())

print("Generating Profiles:")
profiler.profile_all()

print("Done.")
