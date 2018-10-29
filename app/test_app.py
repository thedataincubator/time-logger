
import os
import time
import pytest
from models import Event
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from app import create_app

SECRET = 'Isecret'
DB_NAME = 'test.db'

@pytest.fixture
def client():
    db_url = "sqlite:///" + DB_NAME
    app = create_app(SECRET, db_url)
    app.testing = True
    yield app.test_client()
    os.unlink(DB_NAME)

@pytest.fixture
def sess():
    db_url = "sqlite:///" + DB_NAME
    engine = create_engine(db_url)
    sess = sessionmaker(bind=engine)
    yield sess()

def _test_status(code, resp):
    assert resp.status_code == code

ROUTES = [
    ('/query_name', 'post'),
    ('/add_event', 'put')
]

def test_no_auth(client):
    for route, method in ROUTES:
        _test_status(401, getattr(client, method)(route))

def test_bad_auth(client):
    for route, method in ROUTES:
        _test_status(401, getattr(client, method)(route, data={'SECRET_KEY':'sup'}))

def test_good_auth(client):
    for route, method in ROUTES:
        _test_status(200, getattr(client, method)(route, 
                                                  data={'SECRET_KEY':SECRET,
                                                        'name':"haha"}))
def test_count(client):
    data = {'SECRET_KEY':SECRET,'name':"haha"}
    for i in range(3):
        client.put('/add_event', data=data)
    assert client.post('/query_name', data=data).json == 1
    time.sleep(1)
    data['window'] = 1e-7
    assert client.post('/query_name', data=data).json == 0

def test_multiple_keys(client):
    data = {'SECRET_KEY':SECRET}
    names = ['haha', 'sup', 'todo']
    for name in names:
        data['name'] = name
        client.put('/add_event', data=data)
    for name in names:
        data['name'] = name
        assert client.post('/query_name', data=data).json == 1

def test_unique(client, sess):
    """test failure"""
    data = {'SECRET_KEY':SECRET,'name':"haha"}
    events = [Event(name=data['name'], time=Event.gen_dt(i % 3)) 
              for i in range(6)]
    sess.add_all(events)
    sess.commit()
    assert client.post('/query_name', data=data).json == 3




