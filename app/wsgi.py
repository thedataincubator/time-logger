import os
from app import create_app

application = create_app(os.environ['SECRET_KEY'], 
                 os.environ['DATABASE_URI'])
