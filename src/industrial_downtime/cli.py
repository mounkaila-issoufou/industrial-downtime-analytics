import argparse

from industrial_downtime.orchestration.pipeline import init_db, reset_data, run_pipeline


def main():
    parser = argparse.ArgumentParser(
        prog="industrial-downtime", description="Industrial Downtime Data Platform CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize database structure (DDL only)")
    subparsers.add_parser("reset", help="Reset data (truncate tables)")
    subparsers.add_parser("run", help="Run data pipeline (DML only)")
    subparsers.add_parser("full-refresh", help="Reset + Run full pipeline")

    args = parser.parse_args()

    if args.command == "init":
        init_db()

    elif args.command == "reset":
        reset_data()

    elif args.command == "run":
        run_pipeline()

    elif args.command == "full-refresh":
        reset_data()
        run_pipeline()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
