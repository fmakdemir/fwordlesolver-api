# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
# ARG YOUR_ENV

ENV \
#   YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.0.1


RUN mkdir /app

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN python -m poetry install --only=main --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

# Update database schemas
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 80

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
