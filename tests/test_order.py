import pytest
from flask import g, session
from BigBucks.db import get_db
from BigBucks.order import get_balance,get_assetid

def test_get_balance(client, app):
    # ONLY after register can get intial balance
    response = client.post(
        '/auth/register', data={'username': 'user2', 'password': 'a'}
    )
    
    with app.app_context():
        id = get_db().execute('Select * from user').fetchone()['userid']
        assert get_balance(id) == 1000000
    
def test_get_assetid(app):
    with app.app_context():
        assert get_assetid('AAPL') == 1