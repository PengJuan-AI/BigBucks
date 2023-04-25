import os
import tempfile

import pytest
from BigBucks import create_app
from BigBucks.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'test_data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# For most of the views, a user needs to be logged in. The easiest way to do this in tests is to make a POST request to the login view with the client
#SIP
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='Test1234'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

    def login_admin(self,username='admin1', password='0000'):
        return self._client.post(
            '/adminauth/adminlogin',
            data={'admin_name': username, 'password': password}
        )
    def logout_admin(self):
        return self._client.get('/adminauth/adminlogout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
