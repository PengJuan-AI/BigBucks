INSERT INTO user (username, password, email, date)
VALUES
('test','pbkdf2:sha256:260000$kAEfuhnJoAcpM3E5$4bb466196506dd8739a2eb10532fe45292c2d15484f452c6074c289e0ae51416', '123@duke.edu', '2023-04-20');

INSERT INTO admin (admin_name, password)
VALUES
('admin','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f');

INSERT INTO balance (balance)
VALUES (1000000);

-- INSERT into Assets_data (symbol, history_date, open, high, low, close, adj_close, volume)
-- VALUES ('AAPL', '2023-3-15', 63, 65, 62, 63, 63.5, 1200000),(2,'2023-3-15', 51, 55, 51,52,52.5,1000000);