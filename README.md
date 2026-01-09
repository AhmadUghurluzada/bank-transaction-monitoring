# Bank Transaction Monitoring ETL Project

This project simulates a simplified **bank transaction monitoring system** using synthetic data.  
It demonstrates how customer, account, and transaction data can be generated, processed through an ETL pipeline, and analyzed using visualizations and a basic dashboard.

The main goal is to practice **data modeling, ETL design, and analytical thinking**, not just writing code.

---

## Project Overview

The pipeline follows a standard ETL structure:

1. **Generate** realistic synthetic banking data
2. **Extract** raw datasets
3. **Transform** data using defined business rules
4. **Load** cleaned data into structured outputs
5. **Analyze & Visualize** transaction behavior and risk indicators

---

## Project Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   ├── generate_data.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Data Model
### Customers

Represents bank customers and their associated risk profiles.
Used for customer-level aggregation and compliance logic.

### Accounts

Represents customer-owned bank accounts.
Links customers to transactions and maintains balance and currency context.

### Transactions

The main fact table containing all transaction activity.

### Transaction Flags

Derived table used to identify potentially risky behavior based on defined rules. Flags are generated during the transform stage using business logic such as:

- Large transaction amounts
- Foreign transactions
- High-risk customer activity

## ETL Pipeline
### Extract

Loads generated raw data into pandas DataFrames. No validation is required at this stage because data is synthetically generated with constraints

### Transform
- Applies business rules
- Creates transaction flags
- Performs light sanity checks

Data is copied before transformation to preserve raw inputs.
Null checks and schema validation are intentionally skipped due to controlled data generation logic.

### Load
- Saves processed datasets as CSV files
- Outputs are used by notebooks and dashboards

## Analysis & Visualization

Exploratory analysis is done in Jupyter Notebook, focusing on:
- Transaction distributions
- Currency usage
- Risk flags and patterns
- Customer vs transaction behavior

Plots are intentionally scaled and formatted to reflect realistic transaction ranges.

## Dashboard

A simple interactive dashboard is included to visualize:

- Transaction volumes
- Flag counts
- High-level risk indicators

The dashboard consumes processed CSV outputs produced by the ETL pipeline.


## How to Run
**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Run the ETL pipeline**
```bash
python src/pipeline.py
```
**3. Run analysis**

Open and run:
```bash
notebooks/analysis.ipynb
```

**4. Run dashboard**
```bash
streamlit run dashboard/app.py
```

## Notes

- Data is fully synthetic and generated with realistic constraints
- The project prioritizes correct modeling and reasoning over excessive complexity
- Designed as a learning-focused ETL and analytics project
