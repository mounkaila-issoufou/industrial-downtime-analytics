import argparse
from industrial_downtime.pipeline import main as pipeline_main


def main():
    parser = argparse.ArgumentParser(
        prog="industrial-downtime",

        description="Industrial Downtime Data Pipeline CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("run", help="Run full data pipeline")

    args = parser.parse_args()

    if args.command == "run":
        pipeline_main()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()