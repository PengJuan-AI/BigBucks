INSERT INTO user (username, password)
VALUES
('test','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f');
-- ('jp584', '123456789'),
-- ('user1', '987654321');

INSERT INTO balance (balance)
VALUES (1000000);

INSERT into Assets_info (symbol, name, shares)
VALUES ('AAPL','apple',4800000),('TSLA','tesla',3500000);

INSERT into Assets_data (assetid, date, open, high, low, close, adj_close, volume)
VALUES (1, '2023-3-15', 63, 65, 62, 63, 63.5, 1200000),(2,'2023-3-15', 51, 55, 51,52,52.5,1000000);