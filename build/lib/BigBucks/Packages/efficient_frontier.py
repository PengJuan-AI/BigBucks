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
from .get_weights import get_portfolio_weights


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
    # r_free = 0.03
    return r/v

def draw(R,V):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(5, 5))
    plt.scatter(V, R)
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.show()

def get_port_info(portfolio):
    # portfolio = get_portfolio_weights(id)
    weights = []
    r = []
    for symbol in portfolio.keys():
        weights.append(portfolio[symbol])
        r.append(cal_avg_return(cal_returns(symbol)))
    weights = np.array(weights)
    r = np.array(r)
    # print(portfolio)
    df = pd.DataFrame(data=portfolio, index=range(len(portfolio)))
    # df = pd.DataFrame(data=portfolio)

    port_r = cal_port_return(weights,r)
    port_v = cal_port_volatility(weights, cal_cov(df))
    sharpe = get_sharpe(port_r, port_v)

    return port_r,port_v,sharpe

def get_ef(portfolio):
    # db = get_db()
    r = {}
    avg_r = []
    # portfolio = get_portfolio_weights(id)
    for symbol in portfolio.keys():
        r[symbol] = list(cal_returns(symbol)[symbol])
        avg_r.append(cal_avg_return(cal_returns(symbol)))
        
    df = pd.DataFrame(data=r)
    # W,R,V, risk_return = efficient_frontier(df,100, avg_r)
    W,risk_return = efficient_frontier(df, 100, avg_r)

    return W,risk_return

def get_best_w(df):
    bounds = Bounds(0, 1)  # all weights between (0,1)
    linear_constrain = LinearConstraint(np.ones((df.shape[1],), dtype=int), 1, 1)

    weight = np.ones(df.shape[1])
    x0 = weight / np.sum(weight)  # x0 is the initial guess
    covar = df.cov()
    # Define fun to calculate volatility
    fun = lambda w: np.sqrt(np.dot(w, np.dot(w, covar)))
    res = minimize(fun, x0, method='SLSQP', constraints=linear_constrain, bounds=bounds)

    return res.x

def efficient_frontier(df, num, r):
    
    w0 = get_best_w(df)
    gap = (np.amax(r) - cal_port_return(w0,r))/num
    # port_return = np.zeros(num)
    # port_vol = np.zeros(num)
    port_risk_return = []
    weights = np.zeros((num, len(df.columns)))
    # port_return = []
    # port_vol = []
    # weights = []
    covar = df.cov()
    print("w0: ", w0)

    for i in range(num):
        bounds = Bounds(0, 1)  # all weights between (0,1)
        re = cal_port_return(w0, r) + i * gap
        double_constraint = LinearConstraint([np.ones(df.shape[1]), r], [1, re], [1, re])
        x0 = w0  # x0 is the initial guess
        # Define fun to calculate volatility
        fun1 = lambda w: np.sqrt(np.dot(w, np.dot(w, covar)))
        result = minimize(fun1, x0, method='SLSQP', constraints=double_constraint, bounds=bounds)

        weights[i,:] = result.x
        # port_return[i] = re
        # port_vol[i] = cal_port_volatility(result.x, covar)
        port_risk_return.append([re, cal_port_volatility(result.x, covar)])

    # print("port_risk_return:", port_risk_return)

    # return weights,port_return,port_vol, port_risk_return
    return weights, port_risk_return
