import sqlite3
from datetime import datetime, timedelta
import os
import yfinance as yf

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

        
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    insert_first_admin()
    store_historical_data('SPY')


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def insert_first_admin():
    db = get_db()
    admin_name = "admin1"
    password = "0000"
    db.execute(
        "INSERT INTO admin (admin_name, password) VALUES (?, ?)",
        (admin_name, generate_password_hash(password))
        )
    db.commit()

def store_historical_data(symbol):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    stock_data = yf.download(symbol, start=start_date, end=end_date)

    db = get_db()
    
    for index, row in stock_data.iterrows():
        symbol = symbol
        history_date = index.strftime('%Y-%m-%d')
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        adj_close_price = row['Adj Close']
        volume = row['Volume']

        db.execute("INSERT OR REPLACE INTO Assets_data (symbol, history_date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (symbol, history_date, open_price, high_price, low_price, close_price, adj_close_price, volume))

    db.commit()