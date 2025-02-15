FROM python:3.11.5-alpine

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
WORKDIR /app
COPY / .
RUN poetry install --no-dev --no-root --no-interaction --no-ansi
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input
EXPOSE 80
CMD python manage.py runserver 0.0.0.0:80
