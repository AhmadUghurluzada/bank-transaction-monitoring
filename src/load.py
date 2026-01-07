"""
Load module for saving processed data to CSV and SQLite.
"""

import os
import sqlite3
import pandas as pd

from transform import transform
from extract import extract_accounts, extract_customers


def ensure_directory():
    """
    Create required directories if they do not exist.
    """
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/raw", exist_ok=True)



def load_to_csv(customers_df, accounts_df, transactions_df, flags_df):
    """
    Save processed dataframes to CSV files.
    """
    customers_df.to_csv("data/processed/CSVs/customers.csv", index=False)
    accounts_df.to_csv("data/processed/CSVs/accounts.csv", index=False)
    transactions_df.to_csv("data/processed/CSVs/transactions.csv", index=False)
    flags_df.to_csv("data/processed/CSVs/transaction_flags.csv", index=False)



def load_to_sqlite(customers_df, accounts_df, transactions_df, flags_df):
    """
    DLoad dataframes to a SQLite database.
    """
    conn = sqlite3.connect("data/processed/sqlite/bank_data.db")

    customers_df.to_sql("customers", conn, if_exists="replace", index=False)
    accounts_df.to_sql("accounts", conn, if_exists="replace", index=False)
    transactions_df.to_sql("transactions", conn, if_exists="replace", index=False)
    flags_df.to_sql("transaction_flags", conn, if_exists="replace", index=False)

    conn.close()



def load():
    """
    Main load function to process and save data.
    """
    ensure_directory()

    customers_df = extract_customers()
    accounts_df = extract_accounts()
    transactions_df, flags_df = transform()

    load_to_csv(customers_df, accounts_df, transactions_df, flags_df)
    load_to_sqlite(customers_df, accounts_df, transactions_df, flags_df)



if __name__ == "__main__":
    load()