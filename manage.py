import os
import argparse
from dotenv import load_dotenv
import sys
import colorlog
from pathlib import Path
import uvicorn


def parse_arguments():
    """Parsing args from command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Path to the .env file')
    parser.add_argument('command', help='Command to execute (e.g., runserver, startapp)')
    return parser.parse_args()


def main():
    project_root = Path(__file__).resolve().parent
    sys.path.append(str(project_root) + "/src")
    args = parse_arguments()

    handler = colorlog.StreamHandler()

    logger = colorlog.getLogger(__name__)
    logger.addHandler(handler)
    handler.setFormatter(colorlog.ColoredFormatter('%(red)s%(levelname)s:%(name)s:%(message)s'))

    # Check the command and execute the corresponding logic
    match args.command:
        case "runserver":
            # Run the FastAPI app using uvicorn
            if args.config:
                load_dotenv(dotenv_path=args.config)
            else:
                load_dotenv(dotenv_path="example.env")
                logger.warning(
                    """You using the example config 'example.env' instead use your custom config
                    using --config /path/to/config.env"""
                )
            uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
        case "test": # run testing
            if args.config:
                load_dotenv(dotenv_path=args.config)
            else:
                load_dotenv(dotenv_path="testing/testing.env")
            os.system("pytest ./testing")
        case "lint": # run linting
            os.system("pylint --recursive=y ./src/ ./testing/")
        case _:
            print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
