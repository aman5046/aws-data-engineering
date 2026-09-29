import boto3
import json

REGION = "ap-south-1"
SECRET_NAME = "aws-data-engineering/demo-secret"


def get_secret():
    client = boto3.client(
        "secretsmanager",
        region_name=REGION
    )

    response = client.get_secret_value(
        SecretId=SECRET_NAME
    )

    secret = json.loads(response["SecretString"])

    return secret


if __name__ == "__main__":
    secret = get_secret()

    print("Secret retrieved successfully!")
    print("Available keys:", list(secret.keys()))
    print("Username:", secret["username"])