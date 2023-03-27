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
from Parse_data import parse_data

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

def calculate_avg_return(hist_return):
    return np.average(hist_return)

def calculate_std(hist_return):
    return np.std(hist_return)

def covariance_matrix(assets):
    returns = []
    for asset in assets:
        returns.append(asset.get_returns())

    # return_array = np.array(returns)
    return np.cov(returns)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = parse_data()
    assets = list(data.columns)
    print(assets)

    portfolio = Portfolio()
    for a in assets:
        if a=='Time':
            continue
        else:
            asset = Asset(a, data[[a]])
            asset.print()
            portfolio.add_asset(asset)

    portfolio.print()
    matrix = portfolio.get_covariance_matrix()
    print(matrix)
    portfolio.correlation()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/