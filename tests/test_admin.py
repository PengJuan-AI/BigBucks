import pytest
from flask import g, session
from BigBucks.db import get_db
# from BigBucks.order import get_balance, buy_asset, get_company_name,get_company_shares
from BigBucks.Packages.get_weights import get_all_weights

def test_risk_return(auth, app):
    # auth.login_admin()
    auth.login()

    with app.app_context():
        assert get_all_weights() is None

