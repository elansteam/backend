FROM python:3.12.1-alpine3.19

ARG ELANTS_CONFIG_FILE_PATH

COPY ./pyproject.toml ./pyproject.toml


RUN pip3 install poetry 
RUN poetry install

COPY ./src ./src
COPY $ELANTS_CONFIG_FILE_PATH /elants_config.json
WORKDIR ./src

ENV ELANTS_CONFIG_FILE_PATH=/elants_config.json

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
