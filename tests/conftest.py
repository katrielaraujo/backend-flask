import pytest
from app import app, db


@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('instance.config.TestingConfig')
    testing_client = app.test_client()

    with app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()
