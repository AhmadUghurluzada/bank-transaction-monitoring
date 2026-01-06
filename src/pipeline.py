from extract import extract_accounts, extract_customers
from transform import transform
from load import load


def etl_pipeline():
    """
    Run the complete ETL pipeline
    """
    load()


if __name__ == "__main__":
    etl_pipeline()