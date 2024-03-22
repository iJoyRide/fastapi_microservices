from fastapi import FastAPI, HTTPException, Body
from redis_om import get_redis_connection, HashModel, NotFoundError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
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


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format_product(pk: str):
    try:
        product = Product.get(pk)
    except KeyError:
        return {"message": "Product not found"}

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product_data: dict = Body(...)):
    # Create a new Product instance from the dictionary
    product = Product(**product_data)
    product.save()  # Save the new product to Redis
    return format_product(product.pk)  # Return the formatted product


@app.get('/products/{pk}')
def get(pk: str):
    try:
        product = Product.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.delete('/products/{pk}')
def delete(pk: str):
    try:
        Product.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")

    Product.delete(pk)
    return {"message": "Product deleted successfully"}
