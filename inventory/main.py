from fastapi import FastAPI
from redis_om import get_redis_connection

app = FastAPI()

redis = get_redis_connection()
@app.get("/")
def read_root():
    return {"Hello": "World"}