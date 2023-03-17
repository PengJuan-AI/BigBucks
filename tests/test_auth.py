import pytest
from flask import g, session
from BigBucks.db import get_db

# client_get() makes a GET request, client_post() makes a POST request.
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session