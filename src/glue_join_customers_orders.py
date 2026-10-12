
import sys

from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

# Initialize Glue and Spark
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

# S3 input paths
bucket = "aman-aws-de-2026-bucket1"

customers_path = (
    "s3://aman-aws-de-2026-bucket1/raw/customers/customers.csv"
)

orders_path = (
    "s3://aman-aws-de-2026-bucket1/raw/orders/orders.csv"
)

# Read both CSV files
customers_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(customers_path)
)

orders_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(orders_path)
)

# Normalize column names
customers_df = customers_df.toDF(
    *[c.strip().lower() for c in customers_df.columns]
)
orders_df = orders_df.toDF(
    *[c.strip().lower() for c in orders_df.columns]
)

# Join using customer_id
joined_df = orders_df.join(
    customers_df,
    on="customer_id",
    how="inner"
)

# Print sample records to the job logs
joined_df.show(10, truncate=False)

# Write the result to S3
output_path = (
    f"s3://{bucket}/processed/glue-output/"
)

(
    joined_df.write
    .mode("overwrite")
    .option("header", "true")
    .csv(output_path)
)

print("Customer-orders join completed successfully.")

job.commit()
