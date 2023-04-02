# Accomplishment

1. Handle error in order module
   1. limit user buy order within their balance
   2. search for asset that don't exist
   3. sell shares of asset over the amount they own
   4. if user haven't buy any asset, efficient frontier module shows *"please add asset into your portfolio"*
2. Finish efficient frontier blueprint and templates
3. Finish displaying user-own assets' 5-year data in portfolio module
   1. portfolio tamplate
   2. portfolio route and blueprint
   3. historical data charting
4. Extra completion: administrator interface
   1. admin.py
      1. view_users: overview users' information
      2. view_admin: overview admins' information
      3. add_admin: add new administrator
      4. risk_return: overview all users risk-return profile
      5. today_order: overview all orders in today
      6. account_settings: for admin to modify their information
   2. admin_auth.py
      1. admin login
      2. admin logout
   3. admin templates
