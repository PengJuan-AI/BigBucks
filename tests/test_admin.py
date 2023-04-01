import pytest
from flask import g, session
from BigBucks.db import get_db
# from BigBucks.order import get_balance, buy_asset, get_company_name,get_company_shares
import numpy as np
from BigBucks.Packages.get_weights import get_all_weights

def test_risk_return(auth):
    auth.login_admin()
