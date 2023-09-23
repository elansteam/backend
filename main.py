from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
<<<<<<< HEAD
    return {"message": f"Hello {name}"}
=======
    return {"message": f"Hello {name}"}
>>>>>>> dae180f (starting)
