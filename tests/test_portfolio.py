import pytest
from flask import g, session
from BigBucks.db import get_db
from BigBucks.order import get_balance, buy_asset, get_company_name,get_company_shares
from BigBucks.analysis import get_hist_data

def test_get_hist_data(client, auth, app):
    auth.login()

    with app.appcontext():
        data = get_hist_data('AAPL')
        assert data[0]['date'] == '2023-03-27'