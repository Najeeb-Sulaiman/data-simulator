import os
import json
import random
import uuid
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from tqdm import tqdm
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

    return suppliers


# PRODUCTS
def products(NUM_PRODUCTS: int, DATA_DIR: str, suppliers: list):
    categories = [
        "Electronics", "Home", "Groceries", "Clothing",
        "Beauty", "Sports", "Automotive", "Toys"
        ]

    products = []

    for i in range(NUM_PRODUCTS):

        supplier = random.choice(suppliers)

        products.append({
            "product_id": f"PROD-{i:06d}",
            "product_name": fake.word().capitalize(),
            "category": random.choice(categories),
            "brand": fake.company(),
            "unit_price": round(random.uniform(5, 500), 2),
            "supplier_id": supplier["supplier_id"]
        })

    products_df = pd.DataFrame(products)
    products_df.to_csv(f"{DATA_DIR}/products.csv", index=False)

    print("Products generated")
    return products_df


# STORES
def store(NUM_STORES: int, DATA_DIR: str):
    stores = []

    for i in range(NUM_STORES):

        stores.append({
            "store_id": f"STORE-{i:04d}",
            "store_name": fake.company(),
            "city": fake.city(),
            "state": fake.state(),
            "region": random.choice(["West", "East", "South", "Midwest"]),
            "store_open_date": fake.date_between("-10y", "-1y")
        })

    stores_df = pd.DataFrame(stores)
    stores_df.to_csv(f"{DATA_DIR}/stores.csv", index=False)

    print("Stores generated")
    return stores_df


# WAREHOUSES
def warehouse(NUM_WAREHOUSES: int):
    for i in range(NUM_WAREHOUSES):
        warehouses = []
        warehouses.append({
            "warehouse_id": f"WH-{i:03d}",
            "city": fake.city(),
            "state": fake.state()
        })

    warehouse_df = pd.DataFrame(warehouses)
    return warehouse_df


# INVENTORY SNAPSHOTS
def inventory(DAYS: int,
              DATA_DIR: str,
              START_DATE: datetime,
              products_df,
              warehouse_df):
    for d in range(DAYS):

        snapshot_date = START_DATE + timedelta(days=d)

        rows = []

        for wh in warehouse_df:

            sampled_products = np.random.choice(
                    products_df.product_id,
                    size=2000)

            for p in sampled_products:

                qty = max(0, int(np.random.normal(200, 50)))

                rows.append({
                    "warehouse_id": wh["warehouse_id"],
                    "product_id": p,
                    "quantity_available": qty,
                    "reorder_threshold": random.randint(20, 80),
                    "snapshot_date": snapshot_date.strftime("%Y-%m-%d")
                })

        df = pd.DataFrame(rows)

        df.to_csv(
            f"{DATA_DIR}/warehouse_inventory/inventory_{snapshot_date.date()}.csv",
            index=False
        )

    print("Inventory snapshots generated")


# SHIPMENTS
def shipment(DAYS: int,
             MAX_SHIPMENTS_PER_DAY: int,
             DATA_DIR: str,
             START_DATE: datetime,
             store_df,
             warehouse_df):

    for d in range(DAYS):

        shipment_date = START_DATE + timedelta(days=d)

        records = []

        for _ in tqdm(range(MAX_SHIPMENTS_PER_DAY)):

            product = random.choice(products)
            store = random.choice(store_df)
            warehouse = random.choice(warehouse_df)

            expected = shipment_date + timedelta(days=random.randint(1, 5))

            actual = expected + timedelta(days=random.choice([0, 0, 0, 1, 2]))

            records.append({
                "shipment_id": str(uuid.uuid4()),
                "warehouse_id": warehouse["warehouse_id"],
                "store_id": store["store_id"],
                "product_id": product["product_id"],
                "quantity_shipped": random.randint(5, 200),
                "shipment_date": shipment_date.isoformat(),
                "expected_delivery_date": expected.isoformat(),
                "actual_delivery_date": actual.isoformat(),
                "carrier": random.choice(["FedEx", "UPS", "DHL", "USPS"])
            })

        with open(
            f"{DATA_DIR}/shipments/shipments_{shipment_date.date()}.json",
            "w"
        ) as f:

            json.dump(records, f)

    print("Shipment logs generated")


if __name__ == "__main__":
    # Make directories if not exist
    make_dir(Config.DATA_DIR)

    # Generate suppliers
    suppliers_df = suppliers(Config.NUM_SUPPLIERS)

    # Generate products
    products_df = products(Config.NUM_PRODUCTS, Config.DATA_DIR, suppliers_df)

    # Generate Store
    store_df = store(Config.NUM_STORES, Config.DATA_DIR)

    # Generate Warehouse
    warehouse_df = warehouse(Config.NUM_WAREHOUSES)

    # Generate inventory
    inventory(Config.DAYS, Config.DATA_DIR, Config.START_DATE, products_df, warehouse_df)

    # Generate Shipments
    shipment(Config.DAYS, Config.MAX_SHIPMENTS_PER_DAY, Config.DATA_DIR, Config.START_DATE, store_df, warehouse_df)
