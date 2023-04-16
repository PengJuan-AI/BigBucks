# import pytest
from flask import g, session
from BigBucks.db import get_db

# client_get() makes a GET request, client_post() makes a POST request.
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'user2', 'password': 'a'}
    )
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'user2'",
        ).fetchone() is not None
        # test if the balance is initialized
        id = get_db().execute(
            "SELECT userid FROM user WHERE username = 'user2'",
        ).fetchone()[0]
        assert get_db().execute(
            "SELECT balance FROM Balance WHERE userid = ?", (id,)
        ).fetchone()[0] == 1000000

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    # assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

# @pytest.mark.parametrize(('username', 'password', 'message'), (
#     ('a', 'test', b'Incorrect username.'),
#     ('test', 'a', b'Incorrect password.'),
# ))
# def test_login_validate_input(auth, username, password, message):
#     response = auth.login(username, password)
#     assert message in response.data
    
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
        
