'''
Parsing data files - name hist_return
Calculate each asset's return
Calculate each asset's volatility
Calculate correlation
Calculate covariance
For return xx to xx, calculate the minimum volatility
Draw efficient frontier line
'''
import pandas as pd
import numpy as np
from scipy.optimize import minimize,LinearConstraint,Bounds
# from Parse_data import parse_data
from BigBucks.db import get_db
from Packages.get_weights import get_portfolio_weights


# each stock's return and volatility
def cal_returns(symbol):
    db = get_db()
    period = 5*250
    data = pd.DataFrame(db.execute("SELECT adj_close FROM assets_data WHERE symbol=? "
                                   "ORDER BY history_date DESC LIMIT ?",
                                   (symbol,period)).fetchall(), columns=[symbol]
                        )
    data = data.iloc[::-1]
    p1 = data.iloc[1:, :]
    p0 = data.iloc[0:-1, :]
    returns = np.divide(p1, p0) - 1
    # return np.array(returns)
    return returns

def cal_avg_return(returns):
    return np.mean(np.array(returns))*252

def cal_std(returns):
    # print(np.std(returns))
    return np.std(np.array(returns))

def cal_cov(portfolio):
    returns = {}
    for symbol in portfolio.columns:
        returns[symbol] = list(cal_returns(symbol)[symbol])

    result = pd.DataFrame(data=returns)
    # result.to_excel('test_data.xlsx',sheet_name='returns')
    # print("==============================")
    # print("results:")
    # print(result)
    return result.cov()

def cal_port_return(weight,r):
    # annual
    return np.sum(weight*r)

def cal_port_volatility(weight, cov):
    # annual
    return np.sqrt(((weight.dot(cov)).dot(weight.T)))

def get_sharpe(r,v):
    r_free = 0.03
    return (r-r_free)/v
def draw(R,V):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(5, 5))
    plt.scatter(V, R)
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.show()
    
def get_ef(id):
    # db = get_db()
    r = []
    portfolio = get_portfolio_weights(id)
    for symbol in portfolio.keys():
        # portfolio[symbol] = [portfolio[symbol], cal_avg_return(cal_returns(symbol)),cal_std(cal_returns(symbol))]
        portfolio[symbol] = list(cal_returns(symbol)[symbol])
        r.append(cal_avg_return(cal_returns(symbol)))
    # df = pd.DataFrame(data=portfolio,index=['Weight','Return','Volatility']).T
    df = pd.DataFrame(data=portfolio)
    # print("Portfolio: \n", df)
    print("r:\n",r)
    W,R,V = efficient_frontier(df,100, 0.005, r)
    draw(R,V)
    return W,R,V

def efficient_frontier(df, num, gap, r):

    port_return = np.zeros(num)
    port_vol = np.zeros(num)
    weights = np.zeros((num, len(df.columns)))
    w0 = np.ones(df.shape[1])/df.shape[1]
    covar = df.cov()
    print("w0: ", w0)

    for i in range(num):
        bounds = Bounds(0, 1)  # all weights between (0,1)
        # linear_constrain = LinearConstraint(np.ones((df.shape[1],), dtype=int), 1, 1)
        # re = cal_port_return(r, w0) + i * gap
        re = 0 + i*gap
        double_constraint = LinearConstraint([np.ones(df.shape[1]), r], [1, re], [1, re])
        x0 = w0  # x0 is the initial guess
        # Define fun to calculate volatility
        fun1 = lambda w: np.sqrt(np.dot(w, np.dot(w, covar)))
        result = minimize(fun1, x0, method='SLSQP', constraints=double_constraint, bounds=bounds)

        weights[i,:] = result.x
        port_return[i] = re
        port_vol[i] = cal_port_volatility(result.x, covar)

    # print("Min_weight: ",res.x)
    print("weights:", weights)
    print("port_re:", port_return)
    print("port_vol:", port_vol)
    
    return weights,port_return,port_vol

