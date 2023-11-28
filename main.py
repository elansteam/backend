"""test"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """test"""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    """test"""
    return {"message": f"Hello {name}"}
