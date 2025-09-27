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
ENV UV_PYTHON_CACHE_DIR=/root/.cache/uv/python
# use the system python
ENV UV_SYSTEM_PYTHON=1

RUN mkdir /app

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and uv.lock files
COPY pyproject.toml uv.lock /app/

# Install python and pip with uv, using a cache to speed up subsequent builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install

# Install dependencies with caching
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Copy the rest of the application code
COPY generate_openapi_spec.py /app/
COPY ./fastapi_app/ /app/fastapi_app/

# Expose the port the app runs on
EXPOSE 80

RUN ["uv", "run", "python", "generate_openapi_spec.py"]

# Run the FastAPI application with Uvicorn
CMD ["uv", "run", "uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "80"]
