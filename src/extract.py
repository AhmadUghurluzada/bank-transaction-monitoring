import pandas as pd
from generate_data import customers_df, accounts_df, transactions_df


def extract_customers() -> pd.DataFrame:
    """
    Extract raw customer data
    """
    return customers_df


def extract_accounts() -> pd.DataFrame:
    """
    Extract raw account data
    """
    return accounts_df  


def extract_transactions() -> pd.DataFrame:
    """
    Extract raw transaction data
    """
    return transactions_df


if __name__ == "__main__":
    print("Customers Data:")
    print(extract_customers().head())
    
    print("\nAccounts Data:")
    print(extract_accounts().head())
    
    print("\nTransactions Data:")
    print(extract_transactions().head())
