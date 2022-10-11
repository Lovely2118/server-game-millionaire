import pytest
from starlette.testclient import TestClient

from app.commands import fast_app


@pytest.fixture(scope="function")
def setup():
    client = TestClient(fast_app)
    return client
