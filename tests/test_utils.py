import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.commands import fast_app
from app.database.session import SessionLocal
from app.models.quiz_models import UserModel, BlockModel


@pytest.fixture(scope="function")
def setup():
    client = TestClient(fast_app)
    with SessionLocal() as session:
        block = session.query(BlockModel).filter(BlockModel.id == 1).first()
        test_user = get_test_user(session)
        if test_user is None:
            test_user = UserModel(user_id="test_user_id", name="test_name", money=100, block=block)
            session.add(test_user)
            session.commit()
    return {
        "fast_api_client": client,
        "user_id": "test_user_id"
    }


def teardown():
    with SessionLocal() as session:
        test_user = get_test_user(session)
        if test_user is not None:
            session.delete(test_user)
            session.commit()


def get_test_user(session: Session) -> UserModel:
    test_user = session.query(UserModel).filter(UserModel.user_id == "test_user_id").first()
    return test_user
