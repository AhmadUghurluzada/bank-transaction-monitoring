"""
This module contains transformation and rule-based monitoring of banking transactions.
It applies business rules to flag suspicious activities.
"""

from extract import extract_customers, extract_accounts, extract_transactions
import pandas as pd
import numpy as np
import datetime as dt


def flag_high_value_transactions(transactions: pd.DataFrame, threshold: float=10000.0) -> pd.DataFrame:
    """
    Flag transactions when they are above a certain high-value threshold.

    Args:
        transactions (pd.DataFrame): Raw transactions DataFrame
        threshold (float): Amount above which transactions are flagged

    Returns:
        pd.DataFrame: DataFrame containing transaction flags
    """
    flagged = transactions[transactions["amount"] > threshold].copy()
    flagged["flag_id"] = ["FLAG" + str(i).zfill(6) for i in range(1, len(flagged) + 1)]
    flagged["flag_type"] = "high_value"
    flagged["flag_reason"] = f"Transaction amount exceeds {threshold}"
    flagged["flagged_at"] = dt.datetime.now()

    return flagged[["flag_id", "transaction_id", "flag_type", "flag_reason", "flagged_at"]]



def flag_cross_border_transactions(transactions: pd.DataFrame, accounts: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """
    Flag transactions where the origin and destination countries differ.

    Args:
        transactions (pd.DataFrame): Transaction DataFrame
        accounts (pd.DataFrame): Accounts DataFrame
        customers (pd.DataFrame): Customers DataFrame

    Returns:
        pd.DataFrame: DataFrame containing transaction flags
    """
    # Map account and customer countries
    account_customer_map = accounts.set_index("account_id")["customer_id"].to_dict()
    customer_country_map = customers.set_index("customer_id")["country"].to_dict()

    cross_border_flags = []

    for idx, row in transactions.iterrows():
        cust_id = account_customer_map.get(row["account_id"])
        home_country = customer_country_map[cust_id]
        if row["country"] != home_country:
            cross_border_flags.append({
                "flag_id": f"FLAG{str(len(cross_border_flags)+1).zfill(6)}",
                "transaction_id": row["transaction_id"],
                "flag_type": "cross_border",
                "flag_reason": f"Transaction country {row['country']} differs from home country {home_country}",
                "flagged_at": dt.datetime.now()
            })

    return pd.DataFrame(cross_border_flags)



def flag_frequent_transactions(transactions: pd.DataFrame, max_per_day: int=10) -> pd.DataFrame:
    """
    Flag accounts that make frequent transactions.

    Args:
        transactions (pd.DataFrame): Transaction DataFrame
        max_per_day (int): Maximum allowed transactions per day

    Returns:
        pd.DataFrame: DataFrame containing frequent transaction flags
    """
    # Add transaction date column
    transactions["transaction_day"] = transactions["timestamp"].dt.date 

    flag_records = []

    grouped = transactions.groupby(["account_id", "transaction_day"])
    for (acc_id, day), group in grouped:
        if len(group) > max_per_day:
            for txn_id in group.iterrows():
                flag_records.append({
                    "flag_id": f"FLAG{str(len(flag_records)+1).zfill(6)}",
                    "transaction_id": txn_id,
                    "flag_type": "frequent_tx",
                    "flag_reason": f"More than {max_per_day} transactions on {day}",
                    "flagged_at": dt.datetime.now()
                })

    return pd.DataFrame(flag_records)



def transform():
    """
    Run all transformations rules and generate transaction flags.

    Returns:
        tuple: (cleaned_transactions_df, transaction_flags_df)
    """
    customers_df = extract_customers()
    accounts_df = extract_accounts()
    transactions_df = extract_transactions()

    # Note: Skipped checking null/invalid becuase synthetic data was contolled
    cleaned_transactions = transactions_df.copy()

    flags_high_value = flag_high_value_transactions(transactions_df)
    flag_cross_border = flag_cross_border_transactions(cleaned_transactions, accounts_df, customers_df)
    flags_frequent = flag_frequent_transactions(cleaned_transactions)

    all_flags = pd.concat([flags_high_value, flag_cross_border, flags_frequent], ignore_index=True)
    return cleaned_transactions, all_flags



if __name__ == "__main__":
    cleaned, flags = transform()
    print("=========== Sample Flags ============")
    print(flags.head())
    print("\nTotal flags:", len(flags))