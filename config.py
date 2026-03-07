from pydantic import BaseModel
from datetime import datetime


class Config(BaseModel):
    NUM_PRODUCTS = 5000
    NUM_STORES = 800
    NUM_SUPPLIERS = 300
    NUM_WAREHOUSES = 20

    DAYS = 7

    MAX_DAILY_SALES = 200000
    MAX_SHIPMENTS_PER_DAY = 50000

    START_DATE = datetime(2026, 3, 10)

    DATA_DIR = "data"
