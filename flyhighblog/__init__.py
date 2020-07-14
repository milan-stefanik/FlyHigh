# Importing os to have access to sytem-based functions and variables
import os
# Importing Flask application framework
from flask import Flask
# Importing tools for interacting with MongoDB
from flask_pymongo import PyMongo

# Importing system-based variables in development environment
# env.py file contains secrets and must be included in .gitignore file
# When in development environment, env.py file needs
#   to be uploaded to root folder.
# When deployed, env.py is not present and application
#   gets data directly from system-based variebles
from os import path
if path.exists('env.py'):
    import env

# Creating Flask instance
app = Flask(__name__)


# Configuring Flask app to connect to MongoDB server
# Information are pulled from env.py when in development environment
# Information are pulled from system-based variables when deployed
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_DBNAME'] = os.getenv('DB_NAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

# Setting the PyMongo application object
mongo = PyMongo(app)

# Importing routes.py from flyhighblog folder
# Import is not on the top of file to avoid circular imports
# Import must be done after declaring app variable
# Warning "Module level import not at top of file" can be ignored"
from flyhighblog import routes
