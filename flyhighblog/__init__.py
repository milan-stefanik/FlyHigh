# Importing Flask application framework
from flask import Flask
# Importing tools for interacting with MongoDB
from flask_pymongo import PyMongo
# Importing flask-mail
from flask_mail import Mail
from flyhighblog.config import Config


# Setting the PyMongo application object
mongo = PyMongo()

# Setting the flas-mail application object
mail = Mail()


# Import is not on the top of file to avoid circular imports
# Import must be done after declaring app variable
# Warning "Module level import not at top of file" can be ignored"


def create_app(config_class=Config):
    # Creating Flask instance
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    mail.init_app(app)

    # Importing particular routes.py files from respective subfolders
    #   in flyhighblog folder
    from flyhighblog.main.routes import main
    from flyhighblog.posts.routes import posts
    from flyhighblog.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)

    return app
