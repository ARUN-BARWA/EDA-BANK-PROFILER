import json
from bank_eda_profiler.profiler import BankProfiler
from bank_eda_profiler.config import ReportConfig

def main():
    # Provide the paths to your local banking datasets
    data_sources = {
        "leads": "data/lead_master.parquet",
        "applications": "data/account_application_funnel.parquet",
        "accounts": "data/account_master.parquet",
        "sales": "data/sales_hierarchy.parquet",
        "targets": "data/sales_target_achievement.parquet",
        "transactions": "data/transaction_fact.parquet",
        "campaigns": "data/campaign_master.parquet",
        "vkyc": "data/vkyc_session.parquet",
        "customers": "data/customer_master.parquet",
        "holdings": "data/customer_product_holding.parquet",
        "complaints": "data/service_request_complaint.parquet",
        "events": "data/app_event_log.parquet"
    }

    # Setup the configuration with your column mappings
    config = ReportConfig(
        engine="duckdb",
        privacy_mode=True,
        sample_rows=100000,
        output_dir="test_result",
        column_mapping={
            "leads": {
                "lead_id": "lead_id",
                "created_at": "lead_created_at",
                "region": "region"
            },
            "accounts": {
                "account_id": "account_id",
                "customer_id": "customer_id",
                "open_date": "account_open_date",
                "balance": "avg_monthly_balance"
            }
        }
    )

    print("Initializing Bank EDA Profiler...")
    # Initialize the profiler with the data sources and config
    profiler = BankProfiler(data_sources=data_sources, config=config)

    print("\n--- Checking Dataset Readiness ---")
    readiness = profiler.analyze_dataset_readiness()
    for report_name, details in readiness.items():
        print(f"{report_name}: Ready={details['is_ready']} | Score={details['score']}%")

    print("\n--- Generating Reports ---")
    available_reports = profiler.discover_available_reports()
    print(f"Reports that can be generated: {available_reports}")
    
    if available_reports:
        # Generate the reports
        profiler.generate_possible_reports()
        
        # Export as HTML dashboard
        profiler.generate_html_dashboard()
        print(f"\nSuccess! Reports generated in the '{config.output_dir}' directory.")
        print(f"Open '{config.output_dir}/dashboard.html' (if it exists) to view the results.")
    else:
        print("\nNo standard reports could be fully generated with the provided mappings/fields.")
        print("We found some columns in your dataset that look like they might match the missing required fields.")
        suggestions = profiler.suggest_column_mappings()
        
        # Filter out identical mappings (where they already match perfectly)
        actionable_suggestions = {k: v for k, v in suggestions.items() if k != v}
        
        if actionable_suggestions:
            print("\nSuggested Column Mappings (update your config with these):")
            print("\n  Standard Banking Field         ->  Your Dataset Field")
            print("  " + "-"*60)
            for standard_col, your_col in actionable_suggestions.items():
                print(f"  {standard_col:<30} ->  {your_col}")
                
            print("\nTo fix the readiness score, copy the mappings above into the 'column_mapping' dictionary in this script!")
        else:
            print("\nNo column mapping suggestions could be automatically inferred based on your dataset's columns.")

if __name__ == "__main__":
    main()
