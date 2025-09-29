import argparse
import importlib
import importlib.util
import json
import logging
import sys
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

ROOT_PATH = Path(__file__).parent
MODULE_NAME = "fastapi_app"
MODULE_PATH = ROOT_PATH / MODULE_NAME

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.handlers[0].setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))


def generate_openapi_spec():
    # Path to the FastAPI app
    app_path = MODULE_PATH / "main.py"
    app_module_name = f"{MODULE_NAME}.main"

    try:
        # Dynamically load the FastAPI app
        spec = importlib.util.spec_from_file_location(app_module_name, app_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Ensure the module has an app instance
        if not hasattr(module, "app") or not isinstance(module.app, FastAPI):
            logger.error(f"Couldn't find a FastAPI 'app' instance in the module={module}")
            return

        app = module.app

        # Generate OpenAPI spec
        app
        openapi_spec = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            servers=app.servers,
            summary=app.summary,
            openapi_version=app.openapi_version,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
        )

        # Save the OpenAPI spec as JSON
        # TODO: add yaml output as well
        spec_json = json.dumps(openapi_spec, indent=2)
        output_file = ROOT_PATH / "openapi.json"
        # write with newline for formatter
        output_file.write_text(f"{spec_json}\n")

        logger.info(f"OpenAPI spec has been generated and saved to {output_file}")
    except Exception as e:
        logger.error(f"Failed to generate OpenAPI spec due to error={e}", exc_info=True)


class WatchHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".py"):
            logger.info(f"Detected changes in file: {event.src_path}. Regenerating OpenAPI spec...")
            self.callback()


def watch_mode():
    generate_openapi_spec()

    path = MODULE_PATH.as_posix()
    event_handler = WatchHandler(reload_and_generate)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    logger.info(f"Watching for changes in Python files under {path}/...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def reload_and_generate():
    # Reload all fastapi_app modules
    for name, module in list(sys.modules.items()):
        if name.startswith("fastapi_app") and module:
            try:
                importlib.reload(module)
            except Exception as e:
                logger.error(f"Failed to reload module {name}: {e}")
    generate_openapi_spec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate OpenAPI spec for a FastAPI app.")
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Enable watch mode to regenerate spec on changes.",
    )
    args = parser.parse_args()

    if args.watch:
        watch_mode()
    else:
        generate_openapi_spec()
