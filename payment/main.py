from fastapi import FastAPI, HTTPException, Body
from redis_om import get_redis_connection, HashModel, NotFoundError
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

redis_password = os.getenv("PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-16677.c252.ap-southeast-1-1.ec2.cloud.redislabs.com",
    port=16677,
    password=redis_password,
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending


@app.post('/orders')
async def create(request: Request):
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])

    return req.json()
