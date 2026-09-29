# AWS Data Engineering Hands-on Project

## Overview

This project demonstrates AWS Secrets Manager integration, downloading files from Amazon S3 using Python, and joining two S3 datasets to generate an output file in S3.

## Tasks Completed

### 1. AWS Secrets Manager

* Created a Python program to retrieve secrets from AWS Secrets Manager.
* **File:** `src/secrets_manager.py`

### 2. Download Files from S3

* Created a Python program to download CSV files from Amazon S3 to the local system.
* **File:** `src/s3_download.py`
* **Example local output:** `data/customers.csv`

### 3. Join Two S3 Files

* Read customer and order CSV files from S3 using Python.
* Joined the datasets using `customer_id`.
* Generated and uploaded the resulting CSV file to S3.

**File:** `src/s3_join.py`

**Input files:**

* `s3://aman-aws-de-2026-bucket1/raw/customers/customers.csv`
* `s3://aman-aws-de-2026-bucket1/raw/orders/orders.csv`

**Output file:**

* `s3://aman-aws-de-2026-bucket1/processed/customer_orders.csv`

## Project Structure

```text
aws-data-engineering/
├── src/
│   ├── secrets_manager.py
│   ├── s3_download.py
│   └── s3_join.py
├── data/
├── tests/
├── .gitignore
└── requirements.txt
```

## Technologies Used

* Python
* Amazon S3
* AWS Secrets Manager
* Boto3
* Pandas
* Git and GitHub

## Execution

Run the Python scripts from the project root:

```bash
python src/secrets_manager.py
python src/s3_download.py
python src/s3_join.py
```

