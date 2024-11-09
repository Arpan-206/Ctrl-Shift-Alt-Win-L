from fastapi import FastAPI
from db import *
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()