FROM python:3.12.1-alpine3.19

# WORKDIR .

COPY ./pyproject.toml ./pyproject.toml

RUN pip3 install poetry 
RUN poetry install

COPY ./src ./src

WORKDIR ./src

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
