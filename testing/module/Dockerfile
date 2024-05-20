FROM python:3.12.1-alpine3.19

COPY ../pyproject.toml ./pyproject.toml

RUN pip3 install poetry 
RUN poetry install

COPY ./src ./src
COPY ./testing ./testing

WORKDIR ./testing

CMD ["poetry", "run", "pytest", "-vv"]
