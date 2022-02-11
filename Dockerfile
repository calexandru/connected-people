# -- Initial stage --
FROM python:3.8-slim AS python-base-image
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.8 \
    POETRY_VIRTUALENVS_CREATE=false

# -- Build stage --
FROM python-base-image as prepare-env
# hadolint required shell pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /code
# create a virtual environment where we will install the project dependencies (avoid install warning under ROOT user)
# install poetry in the base python image
RUN python -m venv /code/venv \
    && /code/venv/bin/pip install --no-cache-dir "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock /code/
# install project dependencies
RUN /code/venv/bin/poetry export -f requirements.txt --without-hashes | /code/venv/bin/pip install -r /dev/stdin

# -- Final stage --
FROM prepare-env as api
COPY app /code/app/
COPY manage.py /code/
EXPOSE 5000
# image entrypoint and command
ENTRYPOINT [ "/code/venv/bin/python", "manage.py" ]
CMD ["gunicornserver"]
