"""
CLI for managing the project backend.
Use `python manage.py --help` for more information.
"""
import os
import argparse
import sys
from pathlib import Path
import uvicorn
from loguru import logger


def parse_arguments():
    """Parsing args from command line"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')
    lint_parser = subparsers.add_parser('lint')
    lint_parser.set_defaults(command='lint')

    run_parser = subparsers.add_parser('run')
    run_parser.set_defaults(command='run')
    run_parser.add_argument('--config', help='Path to the .json config file', required=True)

    return parser.parse_args()


def main():  # pylint: disable=missing-function-docstring
    project_root = Path(__file__).resolve().parent
    sys.path.append(str(project_root) + "/src")
    args = parse_arguments()

    # Check the command and execute the corresponding logic
    match args.command:
        case "run":
            # Run the FastAPI app using uvicorn
            if args.config.split("/")[-1].startswith("example"):
                logger.error((
                    f"You are using the example config {args.config} instead of "
                    "your own one. Example config is not meant to be used "
                    "in production for security and other concerns. Please "
                    "create your own config file and run the app using "
                    "--config /path/to/config.json"
                ))
                sys.exit(1)
            # set path to config to env variable
            os.environ["ELANTS_CONFIG_FILE_PATH"] = args.config

            uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True, reload_dirs="./src")
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
