from BigBucks.db import get_db
import pandas as pd
import numpy as np

def get_all_weights():
    weights = {}
    db = get_db()
    pf = db.execute("SELECT symbol, sum(value) from portfolio GROUP BY symbol").fetchall()

    if not pf:
        return None
    else:
        df = pd.DataFrame(pf, columns=['Symbol', 'Value'])
        total_value = np.sum(df['Value'])
        df['weights'] = round(df['Value']/total_value,2)
        weights = df.set_index('Symbol')['weights'].to_dict()
        # print(weights)

    return weights

def get_portfolio_weights(id):
    weights = {}
    db = get_db()
    pf = db.execute("SELECT symbol, value from portfolio WHERE userid=?",(id,)).fetchall()
    print(pf)
    if not pf:
        return None
    else:
        total_value = db.execute("SELECT sum(value) from portfolio GROUP BY userid "
                                 "Having userid=?", (id,)).fetchone()[0]

        for p in pf:
            weights[p[0]] = round(p[1] / total_value, 2)
    print("symbol and weights: ",weights)
    
    return weights