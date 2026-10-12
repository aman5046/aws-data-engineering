
import json
import logging
import sys

import boto3
import snowflake.connector
from awsglue.utils import getResolvedOptions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


def get_secret(secret_name, region):
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def main():
    args = getResolvedOptions(
        sys.argv,
        ["SNOWFLAKE_SECRET_NAME", "SNOWFLAKE_PROCEDURE"]
    )

    secret_name = args["SNOWFLAKE_SECRET_NAME"]
    procedure_name = args["SNOWFLAKE_PROCEDURE"]
    region = "ap-south-1"

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
            network_timeout=60
        )

        logger.info("Snowflake connection established")

        # Only use a trusted procedure name from Glue job parameters.
        # The name must be a fully qualified DATABASE.SCHEMA.PROCEDURE.
        parts = procedure_name.split(".")
        if len(parts) != 3 or not all(
            part.replace("_", "").isalnum() for part in parts
        ):
            raise ValueError(
                "Procedure name must be DATABASE.SCHEMA.PROCEDURE"
            )

        sql = f"CALL {procedure_name}()"

        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            logger.info("Procedure result: %s", result)

        logger.info("Stored procedure completed successfully")

    except Exception:
        logger.exception("Glue-to-Snowflake execution failed")
        raise

    finally:
        if connection is not None:
            connection.close()
            logger.info("Snowflake connection closed")


if __name__ == "__main__":
    main()
