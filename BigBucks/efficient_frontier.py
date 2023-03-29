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
    # returns = pd.DataFrame()
    returns = {}
    for symbol in portfolio.columns:
        returns[symbol] = list(cal_returns(symbol)[symbol])

    result = pd.DataFrame(data=returns)
    # result.to_excel('test_data.xlsx',sheet_name='returns')
    # print("==============================")
    # print("results:")
    # print(result)
    return result.cov()

def port_return(portfolio):
    return np.sum(portfolio['Weight']*portfolio['Return'])

def port_volatility(portfolio):
    cov = cal_cov(portfolio)
    return np.sqrt(((portfolio['Weight'].dot(cov)).dot(portfolio['Weight'].T)))


def efficient_frontier(id):
    db = get_db()
    portfolio = get_portfolio_weights(id)
    for symbol in portfolio.keys():
        portfolio[symbol] = [portfolio[symbol], cal_avg_return(cal_returns(symbol)),cal_std(cal_returns(symbol))]

    print("Portfolio: ", portfolio)
    df = pd.DataFrame(data=portfolio)
    print(df)
    # R = port_return(df)
    cov = cal_cov(df)
    print(cov)


    
class Portfolio:
    '''
    portfolio: userid, assetid, shares, weight
    '''
    def __init__(self):
        self._assets = []

    def add_asset(self, Asset):
        self._assets.append(Asset)

    def portfolio_return(self):
        # need weight
        pass
    def portfolio_volatility(self):
        # need weight
        pass
    # def get_sharpe(self, risk_free):
    def correlation(self):
        matrix = pd.DataFrame([a.get_returns() for a in self._assets]).T
        print(matrix.corr())

    def get_covariance_matrix(self):
        return covariance_matrix(self._assets)

    def print(self):
        for a in self._assets:
            a.print()

class Asset:
    def __init__(self, name, hist):
        self._name = name
        p1 = hist.iloc[1:,:]
        p0 = hist.iloc[0:-1,:]
        returns = np.divide(p1,p0)-1
        # returns = hist.iloc[1:,0]/hist.iloc[0:-1,0]-1
        self.returns = returns[self._name]

    def get_returns(self):
        return self.returns
    def avg_return(self):
        return calculate_avg_return(self.returns)
    def volatility(self):
        return calculate_std(self.returns)

    def print(self):
        print(self._name)


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

