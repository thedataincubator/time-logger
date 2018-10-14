import os
from functools import wraps
from flask import Flask, render_template, request, redirect, jsonify
from models import Event, db

def create_app(secret_key, database_uri):

  app = Flask(__name__)

  SECRET = secret_key

  app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.app = app
  db.init_app(app)
  db.create_all()
  db.session.commit()

  def key_required(func):
    @wraps(func)
    def view(*args, **kwargs):
      if request.form.get('SECRET_KEY') != SECRET:
        return "Not allowed", 401
      return func(*args, **kwargs)
    return view

  @app.route('/add_event', methods=['PUT'])
  @key_required
  def add():
    name = request.form['name']
    # time will be generated automatically by default
    e = Event(name=name)
    db.session.add(e)
    db.session.commit()
    return 'Ok', 200

  @app.route('/query_name', methods=['POST'])
  @key_required
  def query_event():
    name = request.form['name']
    window = float(request.form.get('window', 3)) # in days
    dt = Event.gen_dt(window)
    return jsonify(Event.query
                        .filter_by(name=name)
                        .filter(Event.time > dt)
                        .count())

  return app

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=os.environ['PORT'])
