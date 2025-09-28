import argparse
import logging

import uvicorn


class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # For uvicorn.access, the path is in the 3rd element of args
        if record.name == "uvicorn.access" and record.args and len(record.args) >= 3:
            path = record.args[2]
            if isinstance(path, str) and path.startswith("/health"):
                return False
        return True


logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run the FastAPI server.")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development.")
    args = parser.parse_args()

    # Run Alembic migrations
    uvicorn.run(
        "fastapi_app.main:app",
        host="0.0.0.0",
        port=80,
        log_config="log_config.yaml",
        reload=args.reload,
    )
