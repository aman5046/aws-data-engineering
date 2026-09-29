
import boto3
from pathlib import Path

BUCKET_NAME = "aman-aws-de-2026-bucket1"
S3_KEY = "raw/customers/customers.csv"
REGION = "ap-south-1"

# Save the downloaded file inside the local data folder
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "customers.csv"


def download_s3_file():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    s3 = boto3.client("s3", region_name=REGION)

    s3.download_file(
        BUCKET_NAME,
        S3_KEY,
        str(OUTPUT_FILE)
    )

    print("Download successful!")
    print(f"Downloaded to: {OUTPUT_FILE}")
    print(f"File size: {OUTPUT_FILE.stat().st_size} bytes")


if __name__ == "__main__":
    download_s3_file()