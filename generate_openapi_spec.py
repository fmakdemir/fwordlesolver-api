import yaml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import importlib.util
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


def generate_openapi_spec():
    # Path to the FastAPI app
    app_path = "fastapi_app/main.py"
    app_module_name = "fastapi_app.main"

    try:
        # Dynamically load the FastAPI app
        spec = importlib.util.spec_from_file_location(app_module_name, app_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Ensure the module has an app instance
        if not hasattr(module, "app") or not isinstance(module.app, FastAPI):
            print(
                "Error: The specified module does not contain a FastAPI app instance named 'app'."
            )
            return

        app = module.app

        # Generate OpenAPI spec
        openapi_spec = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Save the OpenAPI spec as YAML
        output_file = "openapi_spec.yaml"
        with open(output_file, "w") as yaml_file:
            yaml.dump(openapi_spec, yaml_file, default_flow_style=False)

        print(f"OpenAPI spec has been generated and saved to {output_file}")
    except Exception as e:
        print(f"Failed to generate OpenAPI spec due to error: {e}")


class WatchHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".py"):
            print(
                f"Detected changes in file: {event.src_path}. Regenerating OpenAPI spec..."
            )
            self.callback()


def watch_mode():
    path = "fastapi_app"
    event_handler = WatchHandler(reload_and_generate)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching for changes in Python files under {path}/...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def reload_and_generate():
    import sys
    import importlib

    # Reload all fastapi_app modules
    for name, module in list(sys.modules.items()):
        if name.startswith("fastapi_app") and module:
            try:
                importlib.reload(module)
            except Exception as e:
                print(f"Failed to reload module {name}: {e}")
    generate_openapi_spec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate OpenAPI spec for a FastAPI app."
    )
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
