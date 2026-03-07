from pydantic import BaseModel
from datetime import datetime


class Config(BaseModel):
    NUM_PRODUCTS: int = 5000
    NUM_STORES: int = 800
    NUM_SUPPLIERS: int = 300
    NUM_WAREHOUSES: int = 20

    DAYS: int = 7

    MAX_DAILY_SALES: int = 200000
    MAX_SHIPMENTS_PER_DAY: int = 50000

    START_DATE: datetime = datetime(2026, 3, 10)

    DATA_DIR: str = "data"
