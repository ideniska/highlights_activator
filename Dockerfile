FROM python:3.10

ENV HOME=/usr/src/app
WORKDIR $HOME

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip poetry

COPY ["pyproject.toml", "poetry.lock", "$HOME/"]

RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-interaction --no-ansi


# RUN adduser 

# USER app

COPY . $HOME

