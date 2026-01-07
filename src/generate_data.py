"""
This script generates synthetic data for bank customers, their accounts,
and transactions. It simulates a realistic banking scenario:
- Customers with different risk ratings
- Accounts linked to customers with various types and currencies
- Transactions with timestamps, types, amounts, and countries

All outputs are stored in pandas DataFrames.
- customer_df: DataFrame containing customer details
- accounts_df: DataFrame containing account details
- transactions_df: DataFrame containing transaction details
"""


import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


# Constants
NUM_CUSTOMERS = 3000
COUNTRIES = ["AZ", "TR", "GE", "DE", "GB", "US"]
CURRENCIES = ["AZN", "USD", "EUR"]

RISK_RATINGS = ["low", "medium", "high"]
RISK_WEIGHTS = [0.75, 0.2, 0.05]

ACCOUNT_TYPES = ["savings", "checking"]
TRANSACTION_TYPES = ["ATM", "POS", "TRANSFER"]



def random_date(start_date, end_date):
    """
    Generate a random datetime between start_date and end_date.
    """
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


#------------------------
# Generate Customers Data
#------------------------

# Generate unique customer IDs
customer_ids = [f"CUST{str(i).zfill(4)}" for i in range(1, NUM_CUSTOMERS + 1)]

# Random full names
first_names = ["Ali", "Leyla", "Elmar", "Aysel", "Mahir", "Nigar", 
               "Tural", "Sevda", "Kamran", "Gulnar", "Ahmed", 
               "Ismayil", "Semed", "Rashad", "Amina"]
last_names = ["Mammadov", "Huseynova", "Aliyev", "Guliyev", 
              "Ismayilova", "Rzayev", "Suleymanov", 
              "Abdullayeva", "Quliyev", "Hasanova"]

full_names = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(NUM_CUSTOMERS)]


# Random dates of birth between 1960-01-01 and 2005-12-31
start_dob = datetime(1960, 1, 1)
end_dob = datetime(2005, 12, 31)
date_of_births = [random_date(start_dob, end_dob).date() for _ in range(NUM_CUSTOMERS)]


# Assign countries with weighted probabilities
countries = random.choices(COUNTRIES, weights=[0.85, 0.05, 0.03, 0.03, 0.02, 0.02], k=NUM_CUSTOMERS)

# Assign risk ratings based on defined weights
risk_ratings = random.choices(RISK_RATINGS, weights=RISK_WEIGHTS, k=NUM_CUSTOMERS)

# Create customers DataFrame
customers_df = pd.DataFrame({
    "customer_id": customer_ids,
    "full_name": full_names, 
    "date_of_birth": date_of_births, 
    "country": countries,
    "risk_rating": risk_ratings
})



#------------------------
# Generate Accounts Data 
#------------------------

# Each customer can have 1-3 accounts
accounts_per_customer = np.random.choice([1, 2, 3], size=NUM_CUSTOMERS, p=[0.4, 0.5, 0.1])
account_customer_ids = np.repeat(customers_df["customer_id"], accounts_per_customer)
num_accounts = len(account_customer_ids)

# Generate unique account IDs
account_ids = [f"ACC{str(i).zfill(5)}" for i in range(1, num_accounts + 1)]

# Random account types, currencies, balances
account_types = [random.choice(ACCOUNT_TYPES) for _ in range(num_accounts)]
currencies = np.random.choice(CURRENCIES, size=num_accounts, p=[0.7, 0.2, 0.1])
balances = np.round(np.random.uniform(100, 100000, size=num_accounts), 2)

# Random opened dates after customer turns 18
opened_dates = []
for cust_id in account_customer_ids:
    dob = customers_df.loc[customers_df["customer_id"] == cust_id, "date_of_birth"].values[0]
    start_date = pd.Timestamp(dob) + pd.DateOffset(years=18)
    end_date = pd.Timestamp(datetime.now())
    opened_dates.append(random_date(start_date, end_date))

# Create accounts DataFrame
accounts_df = pd.DataFrame({
    "account_id": account_ids,
    "customer_id": account_customer_ids,
    "account_type": account_types,
    "currency": currencies,
    "balance": balances,
    "opened_date": opened_dates
})


#---------------------------
# Generate Transactions Data 
#---------------------------

# Each account can have 1-3 transactions
tx_per_account = np.random.choice([1, 2, 3], size=num_accounts, p=[0.2, 0.7, 0.1])
transaction_account_ids = np.repeat(accounts_df["account_id"], tx_per_account)
num_transactions = len(transaction_account_ids)

# Generate unique transaction IDs
transaction_ids = [f"TXN{str(i).zfill(7)}" for i in range(1, num_transactions+1)]

# Random timestamps for today
base_date = datetime.now().date()
timestamps = [datetime.combine(base_date, datetime.min.time()) + 
              timedelta(seconds=random.randint(0, 86399)) for _ in range(num_transactions)]

# Random transaction types
transaction_types  =np.random.choice(TRANSACTION_TYPES, size=num_transactions, p=[0.3, 0.4, 0.3])

# Random amounts (small frequent, medium less, large rare)
amounts = []
for _ in range(num_transactions):
    r = random.random()
    if r < 0.8:
        amounts.append(round(random.uniform(1, 200), 2))
    elif r < 0.95:
        amounts.append(round(random.uniform(200, 2000), 2))
    else:
        amounts.append(round(random.uniform(2000, 20000), 2))

# Map account currencies to transactions
account_currency_map = accounts_df.set_index("account_id")["currency"].to_dict()
transaction_currencies = [account_currency_map[acc_id] for acc_id in transaction_account_ids]

# Map accounts to customers to countries
account_customer_map = accounts_df.set_index("account_id")["customer_id"].to_dict()
customer_country_map = customers_df.set_index("customer_id")["country"].to_dict()


transaction_countries = []

for acc_id in transaction_account_ids:
    cust_id = account_customer_map[acc_id]
    home_country = customer_country_map[cust_id]
    
    if random.random() < 0.85:
        # Most transactions in home country
        transaction_countries.append(home_country)
    else:
        # Some transactions in foreign countries
        foreign = random.choice([c for c in COUNTRIES if c != home_country])
        transaction_countries.append(foreign)

# Create transactions DataFrame
transactions_df = pd.DataFrame({
    "transaction_id": transaction_ids,
    "account_id": transaction_account_ids,
    "timestamp": timestamps,
    "transaction_type": transaction_types,
    "amount": amounts,
    "currency": transaction_currencies,
    "country": transaction_countries

})


# For quick verification
print(customers_df.head())
print(accounts_df.head())
print(transactions_df.head())

print(f"\nTransaction currency distribution:{transactions_df["currency"].value_counts()}")
print(f"\nTransaction country distribution:{transactions_df["country"].value_counts()}")