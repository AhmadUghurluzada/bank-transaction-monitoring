import random
from datetime import datetime, timedelta
import pandas as pd

NUM_CUSTOMERS = 3000
COUNTRIES = ["AZ", "TR", "GE", "DE", "GB", "US"]
CURRENCIES = ["AZN", "USD", "EUR"]

RISK_RATINGS = ["low", "medium", "high"]
RISK_WEIGHTS = [0.75, 0.2, 0.05]

ACCOUNT_TYPES = ["savings", "checking"]
TRANSACTION_TYPES = ["ATM", "POS", "TRANSFER"]


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)
