FROM python:3.12.1-alpine3.19

ARG CONFIG_PATH

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock


RUN pip3 install poetry
RUN poetry install

COPY ./src ./src
COPY $CONFIG_PATH /config.json
WORKDIR /src

ENV CONFIG_PATH=/config.json

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4242"]
