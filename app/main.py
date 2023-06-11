from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import models
from .database import  engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


connectionCounter = 0
while connectionCounter < 5:
    try:
        connection = psycopg2.connect(database="fastapi",user="postgres",
                                    password="SuatPostgres",
                                    host="localhost",
                                    cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Connected to the database")
        break
    except Exception as e:
        print("Failed to connect to the database", e)
        connectionCounter += 1
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World"}




