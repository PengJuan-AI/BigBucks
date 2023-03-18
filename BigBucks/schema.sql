DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS Portfolio;
DROP TABLE IF EXISTS Assets_info;
DROP TABLE IF EXISTS Assets_data;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Balance;

CREATE TABLE user (
  userid INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
--  firstname TEXT NOT NULL,
--   lastname TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Portfolio (
  userid INTEGER NOT NULL,
  assetid INTEGER NOT NULL,
  shares BIGINT NOT NULL,
  FOREIGN KEY(userid) REFERENCES user(userid),
  FOREIGN KEY(assetid) REFERENCES Assets_info(assetid),
  PRIMARY KEY(userid, assetid)
);

CREATE TABLE Assets_info (
  assetid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
  symbol TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  shares BIGINT NOT NULL
);

CREATE TABLE Assets_data (
  assetid INTEGER NOT NULL,
  date DATE NOT NULL,
  open REAL NOT NULL,
  high REAL NOT NULL,
  low REAL NOT NULL,
  close REAL NOT NULL,
  adj_close REAL NOT NULL,
  volume BIGINT NOT NULL,
  FOREIGN KEY(assetid) REFERENCES Assets_info(assetid),
  PRIMARY KEY(assetid, date)
);

CREATE TABLE Orders (
  orderid INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATE NOT NULL,
  userid INTEGER NOT NULL,
  assetid INTEGER NOT NULL,
  quantity REAL NOT NULL,
  price REAL NOT NULL,
  action TEXT NOT NULL,
  FOREIGN KEY(userid) REFERENCES user(userid),
  FOREIGN KEY(assetid) REFERENCES Assets_info(assetid)
);

CREATE TABLE Balance (
  userid INTEGER PRIMARY KEY AUTOINCREMENT,
  balance DECIMAL(16,2) NOT NULL,
  FOREIGN KEY(userid) REFERENCES user(userid)
);
