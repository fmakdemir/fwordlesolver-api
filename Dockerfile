# Use the debian image from the Docker Hub, we don't need python as uv will install it for us
FROM debian:bookworm-slim

# Install uv from Astral's GitHub Container Registry
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random

RUN mkdir /app

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and uv.lock files
COPY pyproject.toml uv.lock /app/

# Install dependencies
RUN uv sync

# Copy the rest of the application code
COPY ./fastapi_app/ /app/fastapi_app/

# Expose the port the app runs on
EXPOSE 80

# Run the FastAPI application with Uvicorn
CMD ["uv", "run", "uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "80"]
