
import boto3
import pandas as pd
from io import BytesIO, StringIO

# AWS configuration
REGION = "ap-south-1"
BUCKET_NAME = "aman-aws-de-2026-bucket1"

CUSTOMERS_KEY = "raw/customers/customers.csv"
ORDERS_KEY = "raw/orders/orders.csv"
OUTPUT_KEY = "processed/customer_orders.csv"

s3 = boto3.client("s3", region_name=REGION)


def read_csv_from_s3(key):
    """Read a CSV file from S3 into a Pandas DataFrame."""
    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    df = pd.read_csv(BytesIO(response["Body"].read()))
    print(f"Read {len(df)} rows from {key}")
    return df


def join_and_upload():
    # 1. Read both files from S3
    customers_df = read_csv_from_s3(CUSTOMERS_KEY)
    orders_df = read_csv_from_s3(ORDERS_KEY)

    # 2. Join customers and orders using customer_id
    result_df = pd.merge(
        orders_df,
        customers_df,
        on="customer_id",
        how="inner"
    )

    # 3. Convert the joined DataFrame to CSV in memory
    csv_buffer = StringIO()
    result_df.to_csv(csv_buffer, index=False)

    # 4. Upload the output CSV to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=OUTPUT_KEY,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )

    print(f"Join completed. Output rows: {len(result_df)}")
    print(f"Output uploaded to s3://{BUCKET_NAME}/{OUTPUT_KEY}")
    print(result_df.to_string(index=False))


if __name__ == "__main__":
    join_and_upload()