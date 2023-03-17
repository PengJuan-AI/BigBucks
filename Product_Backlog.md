# Product Backlog
1. Design a prototype  
    1. interface
    2. interaction
2. design database schema
3. Design file structure (blueprints) 
    1. template→auth
4. login/register for user
    1. login/register web page (template)
    2. login/register blueprint
    3. user table
    4. testing
5. login/register for admin (web page)
6. buy and sell shares of assets
    1. transaction web page (post a form of transaction info to back end)
    2. transaction blueprint (place order)
        - buy
        - sell
    3. get price using market price/hist price
    4. transaction table
    5. data_hist table
7. display assets’ history data (5 years)
    1. each stock held by account holders (download data)
    2. 5 years SPY index data
    3. data chart web page
    4. SPY index data table
8. analyze the risk-return profile
    1. risk-profile web page
    2. risk return blueprint
        - calculate the volatility for a range of return targets
        - create the function as a python package
            - risk
            - volatility
            - efficiency frontier
    3. sharpe ratio
        - using US Treasury 10-year bond yield as risk-free rate
    4. Enable administrators to analyze the overall risk-return profile
9. run reports on their holdings
    1. List stocks in portfolio—user (web page)
    2. list stocks of all users—admin (web page)
    3. list summary of current day’s market orders across all users — admin (web page)
10. advanced charting features
    1. price plot
    2. returns plots
    3. stock price versus index price chart
    4. stock return vs. index return time series
    5. scatter plot of stock return vs. index return
    6. efficient frontier of the portfolio
