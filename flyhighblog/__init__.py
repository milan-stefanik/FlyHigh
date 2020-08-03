# Importing Flask application framework
from flask import Flask
# Importing tools for interacting with MongoDB
from flask_pymongo import PyMongo
# Importing flask-mail
from flask_mail import Mail
# Importing application config details
from flyhighblog.config import Config


# Setting the PyMongo application object
mongo = PyMongo()

# Setting the flask-mail application object
mail = Mail()


# Creating app with all the required parameters
def create_app(config_class=Config):
    
    # Creating Flask instance
    app = Flask(__name__)
    
    # Importing application config details
    app.config.from_object(Config)

    # Initializing mongo application object
    mongo.init_app(app)
    
    # Initializing flask-mail application object
    mail.init_app(app)

    # Importing particular routes.py files from respective subfolders
    #   in flyhighblog folder (Blueprint)
    from flyhighblog.main.routes import main
    from flyhighblog.posts.routes import posts
    from flyhighblog.users.routes import users
    from flyhighblog.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app
