from __future__ import annotations

import os

import boto3
import pytest
from moto import mock_aws

# Enable the local bearer-token auth fallback for tests.
os.environ["TRIPEVENT_DEBUG"] = "true"
os.environ["TRIPEVENT_TABLE_NAME"] = "tripevent-app-test"


@pytest.fixture()
def dynamodb_table():
    with mock_aws():
        client = boto3.resource("dynamodb", region_name="us-east-1")
        table = client.create_table(
            TableName="tripevent-app-test",
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        table.wait_until_exists()
        yield table


@pytest.fixture()
def client(dynamodb_table):
    # Import inside the fixture so the moto mock is active and the repo singleton
    # is created against the mocked table.
    import app.db as db
    from app.config import settings
    from fastapi.testclient import TestClient

    settings.debug = True
    settings.table_name = "tripevent-app-test"
    db._repo = None  # reset singleton so it binds to the mocked table

    from app.main import app

    return TestClient(app)


def auth(sub: str) -> dict[str, str]:
    """Local dev auth header — the debug fallback treats the bearer value as the sub."""
    return {"Authorization": f"Bearer {sub}"}
