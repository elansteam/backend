"""
CLI for managing the project backend.
Use `python manage.py --help` for more information.
"""
import os
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
import colorlog
import uvicorn


def parse_arguments():
    """Parsing args from command line"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')
    lint_parser = subparsers.add_parser('lint')
    lint_parser.set_defaults(command='lint')

    run_parser = subparsers.add_parser('run')
    run_parser.set_defaults(command='run')
    run_parser.add_argument('--config', help='Path to the .env file', required=True)

    test_parser = subparsers.add_parser('test')
    test_parser.set_defaults(command='test')
    test_parser.add_argument('--config', help='Path to the .env file', required=True)
    return parser.parse_args()


def main():  # pylint: disable=missing-function-docstring
    project_root = Path(__file__).resolve().parent
    sys.path.append(str(project_root) + "/src")
    args = parse_arguments()

    handler = colorlog.StreamHandler()

    logger = colorlog.getLogger(__name__)
    logger.setLevel(colorlog.INFO)
    logger.addHandler(handler)
    handler.setFormatter(colorlog.ColoredFormatter('%(red)s%(levelname)s:%(name)s:%(message)s'))

    # Check the command and execute the corresponding logic
    match args.command:
        case "run":
            # Run the FastAPI app using uvicorn
            if args.config.endswith("example.env"):
                logger.error((
                    "You are using the example config 'example.env' instead of "
                    "your own one. Example config is not meant to be used "
                    "in production for security and other concerns. Please "
                    "create your own config file and run the app using "
                    "--config /path/to/config.env"
                ))
                sys.exit(1)
            load_dotenv(dotenv_path=args.config)
            uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
        case "test":  # run testing
            if args.config:
                load_dotenv(dotenv_path=args.config)
            else:
                load_dotenv(dotenv_path="testing/testing.env")
            os.system("pytest ./testing")
        case "lint":  # run linting
            logger.info("Running pylint...")
            os.system("pylint --recursive=y ./src/ ./testing/")
            logger.info("Running ruff...")
            os.system("ruff .")
            logger.info("Running mypy...")
            os.system("mypy ./src/ ./testing/")
        case _:
            print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
