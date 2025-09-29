# Use the debian image from the Docker Hub, we don't need python as uv will install it for us
FROM debian:bookworm-slim

# Install uv from Astral's GitHub Container Registry
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set some sensible python defaults variables
# - PYTHONFAULTHANDLER: enable faulthandler by default
# - PYTHONUNBUFFERED: disable output buffering
# - PYTHONHASHSEED: randomize hash seeds
ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random
# generate .pyc files
ENV UV_COMPILE_BYTECODE=1
# use copy mode for linking packages (silence warning)
ENV UV_LINK_MODE=copy
# enable caching for the managed python
ENV UV_PYTHON_CACHE_DIR=/uv-cache/python
ENV UV_CACHE_DIR=/uv-cache
# use the system python
ENV UV_SYSTEM_PYTHON=1

RUN mkdir /app
RUN mkdir /uv-cache

# Set the working directory
WORKDIR /app

# Copy dependency and config files
COPY pyproject.toml uv.lock log_config.yaml /app/

# Install dependencies with caching
RUN --mount=type=cache,target=/uv-cache \
    uv sync

# Copy the rest of the application code
COPY *.py /app/
COPY ./fastapi_app/ /app/fastapi_app/

# Expose the port the app runs on
EXPOSE 80

RUN ["uv", "run", "python", "generate_openapi_spec.py"]

# Run the FastAPI application with Uvicorn
CMD ["uv", "run", "python", "server.py"]
