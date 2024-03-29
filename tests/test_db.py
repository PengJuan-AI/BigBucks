import pytest
import sqlite3
from flaskr.db import get_db

# Should return the same connection each time it's called.
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
        
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT user1')
        
    assert 'closed' in str(e.value)

# the init-db command should call the init_db function and output a message
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('BigBucks.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called