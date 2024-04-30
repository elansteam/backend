"""
CLI for managing the project backend.
Use `python manage.py --help` for more information.
"""
import os
import argparse
import sys
from pathlib import Path
from loguru import logger


def parse_arguments():
    """Parsing args from command line"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')
    lint_parser = subparsers.add_parser('lint')
    lint_parser.set_defaults(command='lint')

    return parser.parse_args()


def main():  # pylint: disable=missing-function-docstring
    project_root = Path(__file__).resolve().parent
    sys.path.append(str(project_root) + "/src")
    args = parse_arguments()

    # Check the command and execute the corresponding logic
    match args.command:
        case "lint":  # run linting
            logger.info("Running pylint...")
            os.system("pylint --recursive=y ./src/")
            logger.info("Running ruff...")
            os.system("ruff src/")
            logger.info("Running mypy...")
            os.system("mypy --strict ./src/")
        case _:
            print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
