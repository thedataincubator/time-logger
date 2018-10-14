import os
from app import app as create_app

app = create_app(os.environ['SECRET_KEY'], 
                 os.environ['DATABASE_URI'])
