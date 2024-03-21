from fastapi import FastAPI, HTTPException
from redis_om import get_redis_connection, HashModel, NotFoundError
from fastapi.middleware.cors import CORSMiddleware
import os


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


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    try:
        Product.get(pk)
    except NotFoundError:
        return {"message": "Product does not exist"}


@app.delete('/products/{pk}')
def delete(pk: str):
    try:
        Product.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")

    # If the product exists, proceed with deletion
    Product.delete(pk)
    return {"message": "Product deleted successfully"}
