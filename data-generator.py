import os
import json
import random
import uuid
import numpy as np
import pandas as pd
from faker import Faker
from config import Config


fake = Faker()


def make_dir(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(f"{DATA_DIR}/warehouse_inventory", exist_ok=True)
    os.makedirs(f"{DATA_DIR}/shipments", exist_ok=True)


# SUPPLIERS
def suppliers(NUM_SUPPLIERS: int):
    suppliers = []
    for i in range(NUM_SUPPLIERS):
        suppliers.append({
            "supplier_id": f"SUP-{i:05d}",
            "supplier_name": fake.company(),
            "country": fake.country()
        })

    suppliers_df = pd.DataFrame(suppliers)
    return suppliers_df


# PRODUCTS
def products(NUM_PRODUCTS: int, DATA_DIR: str):
    categories = [
        "Electronics","Home","Groceries","Clothing",
        "Beauty","Sports","Automotive","Toys"
        ]

    products = []

    for i in range(NUM_PRODUCTS):

        supplier = random.choice(suppliers)

        products.append({
            "product_id": f"PROD-{i:06d}",
            "product_name": fake.word().capitalize(),
            "category": random.choice(categories),
            "brand": fake.company(),
            "unit_price": round(random.uniform(5,500),2),
            "supplier_id": supplier["supplier_id"]
        })

    products_df = pd.DataFrame(products)
    products_df.to_csv(f"{DATA_DIR}/products.csv",index=False)

    print("Products generated")


# STORES
def store(NUM_STORES: int, DATA_DIR: str):
    stores = []

    for i in range(NUM_STORES):

        stores.append({
            "store_id": f"STORE-{i:04d}",
            "store_name": fake.company(),
            "city": fake.city(),
            "state": fake.state(),
            "region": random.choice(["West","East","South","Midwest"]),
            "store_open_date": fake.date_between("-10y","-1y")
        })

    stores_df = pd.DataFrame(stores)
    stores_df.to_csv(f"{DATA_DIR}/stores.csv",index=False)

    print("Stores generated")
