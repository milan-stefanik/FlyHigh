import os
from flask import Flask
from flask_pymongo import PyMongo


from os import path
if path.exists('env.py'):
    import env


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_DBNAME'] = os.getenv('DB_NAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

from flyhighblog import routes
