from BigBucks.db import get_db
import pandas as pd

def get_portfolio_weights(id):
    weights = {}
    db = get_db()
    pf = db.execute("SELECT symbol, value from portfolio WHERE userid=?",(id,))
    total_value = db.execute("SELECT sum(value) from portfolio GROUP BY userid "
                             "Having userid=?", (id,)).fetchone()[0]
    
    for p in pf:
        weights[p[0]] = round(p[1]/total_value,2)
    # print(weights)
    
    return weights