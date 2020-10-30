FROM python:3.8.6-alpine3.12 as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base

RUN wget -O - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev


FROM python-base as development
ENV FASTAPI_ENV=development
WORKDIR $PYSETUP_PATH

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN apk add --no-cache --update gcc musl-dev
RUN poetry install

WORKDIR /code/

EXPOSE 8000
CMD ["/code/entrypoint-dev.sh"]


FROM python-base as production
ENV FASTAPI_ENV=production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /code/
WORKDIR /code/
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--host", "0.0.0.0", "--port", "8000", "myproject.asgi:application"]
