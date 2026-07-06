import argparse
import json
from .profiler import BankProfiler
from .profiling.fg_profile import is_fg_available

def main():
    parser = argparse.ArgumentParser(description="Bank EDA Profiler CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # profile
    profile_parser = subparsers.add_parser("profile")
    profile_parser.add_argument("--config", required=True, help="Path to report_config.yaml")
    
    # check-requirements
    req_parser = subparsers.add_parser("check-requirements")
    req_parser.add_argument("--config", required=True)
    req_parser.add_argument("--report", required=True)
    
    # dashboard
    dash_parser = subparsers.add_parser("dashboard")
    dash_parser.add_argument("--config", required=True)
    dash_parser.add_argument("--type", default="all")
    
    # export-excel
    excel_parser = subparsers.add_parser("export-excel")
    excel_parser.add_argument("--config", required=True)
    
    # export-bi
    bi_parser = subparsers.add_parser("export-bi")
    bi_parser.add_argument("--config", required=True)

    # inspect
    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--config", required=True)

    # suggest-mappings
    mappings_parser = subparsers.add_parser("suggest-mappings")
    mappings_parser.add_argument("--config", required=True)

    # discover-reports
    discover_parser = subparsers.add_parser("discover-reports")
    discover_parser.add_argument("--config", required=True)

    # generate-possible
    gen_pos_parser = subparsers.add_parser("generate-possible")
    gen_pos_parser.add_argument("--config", required=True)

    # generate-report
    gen_rep_parser = subparsers.add_parser("generate-report")
    gen_rep_parser.add_argument("--config", required=True)
    gen_rep_parser.add_argument("--report", required=True)

    # fg-profile
    fg_parser = subparsers.add_parser("fg-profile")
    fg_parser.add_argument("--config", required=True)
    fg_parser.add_argument("--table", required=True)

    # fg-profile-all
    fg_all_parser = subparsers.add_parser("fg-profile-all")
    fg_all_parser.add_argument("--config", required=True)
    
    args = parser.parse_args()
    
    profiler = BankProfiler.from_config(args.config)
    
    if args.command == "profile":
        profiler.profile_all()
    elif args.command == "check-requirements":
        res = profiler.check_requirements(args.report)
        print(res.to_text())
    elif args.command == "inspect":
        readiness = profiler.analyze_dataset_readiness()
        print(json.dumps(readiness, indent=2))
    elif args.command == "suggest-mappings":
        suggestions = profiler.suggest_column_mappings()
        print(json.dumps(suggestions, indent=2))
    elif args.command == "discover-reports":
        available = profiler.discover_available_reports()
        print(f"Available reports: {available}")
    elif args.command == "generate-possible":
        reports = profiler.generate_possible_reports()
        print(f"Generated reports: {reports}")
    elif args.command == "generate-report":
        profiler.generate_report(args.report)
        print(f"Generated report: {args.report}")
    elif args.command == "fg-profile":
        res = profiler.generate_fg_profile(args.table)
        if is_fg_available():
            print(f"Generated fg-data-profiling report for {args.table}.")
        else:
            print(f"fg-data-profiling is not installed. Generated fallback DuckDB/Polars profile for {args.table}. Install with: pip install bank_eda_profiler[fg]")
    elif args.command == "fg-profile-all":
        res = profiler.generate_fg_profile_all()
        if is_fg_available():
            print(f"Generated fg-data-profiling reports for all tables.")
        else:
            print(f"fg-data-profiling is not installed. Generated fallback DuckDB/Polars profile for all tables. Install with: pip install bank_eda_profiler[fg]")
    elif args.command == "dashboard":
        if args.type == "all":
            profiler.profile_all()
            profiler.generate_daily_sales_dashboard()
            profiler.generate_kyc_dropoff_report()
            profiler.generate_activation_quality_report()
            profiler.generate_salesperson_productivity_report()
            profiler.generate_dormancy_report()
            profiler.generate_campaign_performance_report()
            profiler.generate_funnel_analysis()
            profiler.generate_cohort_analysis()
            profiler.generate_customer_segmentation()
        elif args.type == "daily_sales":
            profiler.generate_daily_sales_dashboard()
        profiler.generate_html_dashboard()
    elif args.command == "export-excel":
        profiler.profile_all()
        profiler.generate_daily_sales_dashboard()
        profiler.generate_kyc_dropoff_report()
        profiler.generate_activation_quality_report()
        profiler.generate_salesperson_productivity_report()
        profiler.generate_dormancy_report()
        profiler.generate_campaign_performance_report()
        profiler.generate_funnel_analysis()
        profiler.generate_cohort_analysis()
        profiler.generate_customer_segmentation()
        profiler.export_excel()
    elif args.command == "export-bi":
        profiler.profile_all()
        profiler.generate_daily_sales_dashboard()
        profiler.generate_kyc_dropoff_report()
        profiler.generate_activation_quality_report()
        profiler.generate_salesperson_productivity_report()
        profiler.generate_dormancy_report()
        profiler.generate_campaign_performance_report()
        profiler.generate_funnel_analysis()
        profiler.generate_cohort_analysis()
        profiler.generate_customer_segmentation()
        profiler.export_bi_ready_files()

if __name__ == "__main__":
    main()
