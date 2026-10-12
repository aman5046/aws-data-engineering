
import json
import logging
import os

import boto3
import snowflake.connector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_secret(secret_name, region):
    """Retrieve Snowflake credentials from AWS Secrets Manager."""
    client = boto3.client("secretsmanager", region_name=region)

    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def main():
    region = os.environ.get("AWS_REGION", "ap-south-1")
    secret_name = os.environ["SNOWFLAKE_SECRET_NAME"]
    procedure_name = os.environ["SNOWFLAKE_PROCEDURE"]

    credentials = get_secret(secret_name, region)
    connection = None

    try:
        logger.info("Connecting to Snowflake")

        connection = snowflake.connector.connect(
            account=credentials["account"],
            user=credentials["user"],
            password=credentials["password"],
            warehouse=credentials["warehouse"],
            database=credentials["database"],
            schema=credentials["schema"],
            role=credentials.get("role"),
            login_timeout=30,
        )

        logger.info("Connected to Snowflake")

        # Configure this as a trusted, fully qualified procedure name.
        sql = f"CALL {procedure_name}()"

        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            logger.info("Stored procedure result: %s", result)

        logger.info("Stored procedure executed successfully")

    except Exception:
        logger.exception("Snowflake stored procedure execution failed")
        raise

    finally:
        if connection is not None:
            connection.close()
            logger.info("Snowflake connection closed")


if __name__ == "__main__":
    main()
