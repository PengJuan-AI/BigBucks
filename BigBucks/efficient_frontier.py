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
    return np.average(np.array(returns))

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
    return np.sum(weight*r)*252

def cal_port_volatility(weight, cov):
    # annual
    # cov = cal_cov(portfolio.T)
    return np.sqrt(((weight.dot(cov)).dot(weight.T))*252)

def get_sharpe(r,v):
    r_free = 0.03
    return (r-r_free)/v

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
    print("Portfolio: \n", df)
    efficient_frontier(df,10, 0.1, r)
    # R = port_return(df)
    # V = port_volatility(df)
    # print('R: ',R, 'V: ',V)

    # return R,V
    return 0.2, 0.5

def efficient_frontier(df, num, gap, r):

    port_return = np.zeros(num)
    port_vol = np.zeros(num)
    weights = np.zeros((num, len(df.columns)))
    w0 = np.ones(df.shape[1])/df.shape[1]

    for i in range(num):
        bounds = Bounds(0, 1)  # all weights between (0,1)
        # linear_constrain = LinearConstraint(np.ones((df.shape[1],), dtype=int), 1, 1)
        re = cal_port_return(r, w0) + i * gap
        double_constraint = LinearConstraint([np.ones(df.shape[1]), r], [1, re], [1, re])
        x0 = w0  # x0 is the initial guess
        covar = df.cov()
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
    
def covariance_matrix(assets):
    returns = []
    for asset in assets:
        returns.append(asset.get_returns())

    # return_array = np.array(returns)
    return np.cov(returns)

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     data = parse_data()
#     assets = list(data.columns)
#     print(assets)
# 
#     portfolio = Portfolio()
#     for a in assets:
#         if a=='Time':
#             continue
#         else:
#             asset = Asset(a, data[[a]])
#             asset.print()
#             portfolio.add_asset(asset)
# 
#     portfolio.print()
#     matrix = portfolio.get_covariance_matrix()
#     print(matrix)
#     portfolio.correlation()

