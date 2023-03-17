##Requirement 1    
Requirement Type:Function        
Event/User Case #:
1. Users create account
2. Description: Enable customers to create accounts.
3. Login/logout

Rationale: For users to use your website, you should let them create accounts first. With an available account, users can interact with the website and use its multiple functions.  
Originator: customers  
Fit Criterion:
1. New users create an account
   1. user info is stored
2. login
   1. new user need create account
   2. wrong username/password message
3. Interface for sign up and login (web page)
4. Account information is recorded in database

Customer Satisfaction: 5  
Customer Dissatisfaction:  5     
Conflict:
Priority: 5/5    

## Requirement 2     
Requirement Type:Function  
Event/User Case #: Account holder buy and sell shares of stock(s)  
Description: Enable users to buy and sell shares of stocks  
Rationale: Buy and sell is one of the basic functions of BigBucks, which is also the fundamental needs of users.  
Originator: users  
Fit Criterion:
1. Interface for buy and sell (web page)
2. After buy/sell operation for certain amount of shares of stock, corresponding amount of shares are added/deducted from users' account -- update stock data
3. For buy operation, total value of shares of stock must be less than or equal to the balance in user's account -- set limitation
4. For sell operation, the total amount of shares must be less than or equal to the amount of shares that users hold in their account.  
5. get market price   

Customer Satisfaction: 5     Customer Dissatisfaction: 5  
Conflict: None  
Priority: 5/5  

## Requirement 3  
Requirement Type:Function      
Event/User Case #: Track users' transactions  
Description: Record each confirmed transactions.  
Rationale: All transactions must be recorded for further review and evaluation.  
Originator: users, developer  
Fit Criterion:
1. After users' several trading operations, there should be a history of all trades, including buyer/seller amount of shares, stock's close price, total value, and time. -- **transactiom table**
2. Transactions history can be visited only by users themselves.  (web page)

Customer Satisfaction: 4   Customer Dissatisfaction:  5  
Conflict:
Priority: 4/5  

Requirement #:4  
Requirement Type: Function  
Event/User Case #: Users want to consider stock's history and evaluate their holdings   
Description: Enable customers to consider history as they evaluate their holdings.  
Rationale: Historical data of each stock can help users make trading decisions.  
Originator: Users
Fit Criterion:
1. Each stock in users' portfolio has a least five years daily historical data
   1. download data
   2. display charts
   3. **portfolio**
2. SPY index daily data in at least five years
   1. **index_data**

Customer Satisfaction: 4    Customer Dissatisfaction: 5  
Conflict:
Priority:4/5

## Requirement 5  
Requirement Type:Function        
Event/User Case #: Users want to analyze the risk-return profile of their portfolio.  
Description: Enable customers to analyze the risk-return profile of their portfolio.  
Rationale: Risk-return profile can help customers to evaluate their portfolio and help them make trading decisions.  
Originator: Users  
Fit Criterion:
1. Given a certain stock portfolio, calculate the volatility for a range of return targets. 
   1. profile format (web page)
2. Calculate the Sharpe ratio for customer's account, using US treasury 10 year bond yield as the risk-free rate.
3. provide a page for risk-return report to customers.

Customer Satisfaction: 4     Customer Dissatisfaction: 3    
Conflict:  
Priority: 4/5  

## Requirement 6  
Requirement Type:Function        
Event/User Case #: Administrators want to analyze the risk-return profile of their portfolio.  
Description: Enable administrators to analyze the risk-return profiles of all portfolios.  
Rationale: Administrator is able to analyze the overall risk-return profile considering all stocks held by all account holders to avoid kinds of problem of Robinhood in January 2021.   
Originator: administrator  
Fit Criterion:
1. Administrator account can access the overall risk-return profile.

Customer Satisfaction: 2     Customer Dissatisfaction: 2    
Conflict:  
Priority: 3/5  
Supporting Materials:  
History:

## Requirement 7  
Requirement Type: Function     
Event/User Case #: customer wants to see their holdings' report.  
Description: enable customer to run reports on their holdings.  
Rationale: Holding's report can help users briefly review their holdings.  
Originator: users  
Fit Criterion:
1. The report should list stocks owned by ticker symbol, name, shares held, and price per share for customer accounts. 
   1. web page

Customer Satisfaction: 2     Customer Dissatisfaction: 4   
Conflict:  
Priority: 3/5    

## Requirement 8  
Requirement Type: Function     
Event/User Case #: administrator analyzes the whole portfolio in BigBucks system  
Description: enable administrator to run reports on the entire holdings.  
Rationale: Holding's report can help administrator briefly review holdings in BigBucks system.  
Originator: administrator  
Fit Criterion:
1. The report should list stocks across all users by ticker symbol, name, shares held, and price per share for administrator account.  
2. The report should list summary of current day's market orders across all users by ticker symbol, name, shares bought and shares sold.  

Customer Satisfaction: 2     Customer Dissatisfaction: 2   
Conflict:  
Priority: 3/5    

## Requirement 9  
Requirement Type: function       
Event/User Case #: Provide the efficient frontier of account holders' portfolios.  
Description: Given a portfolio, calculate its efficient frontier.  
Rationale: Efficient frontier is a way to evaluate a portfolio.

Originator: users  
Fit Criterion:Given a portfolio, calculate its efficient frontier.  
Customer Satisfaction: 4     Customer Dissatisfaction: 3  
Conflict:  
Priority: 2/5  

## Requirement 10  
Requirement Type: UI/UX Design     
Event/User Case #: Users want to check stocks' historical price or return of their portfolio compared to index.  
Description: Provide customers with advanced charting features, including price plot, returns plots, and prices comparison plots.  
Rationale:
1. Charts can help users directly review stocks' performance and extract information from comparison between stocks or indexes.  

Originator: users  
Fit Criterion:
1. generate price plots and returns plots for account holders.
2. provide stock price versus index price chart
3. provide stock return versus index return chart
4. provide chart for the efficient frontier of account holders' portfolio for a range of return targets and current weights of their holdings.

Customer Satisfaction: 4     Customer Dissatisfaction: 3  
Conflict:  
Priority: 4/5  
