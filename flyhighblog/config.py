# Importing os to have access to sytem-based functions and variables
import os

# Importing system-based variables in development environment
# env.py file contains secrets and must be included in .gitignore file
# When in development environment, env.py file needs
#   to be uploaded to root folder.
# When deployed, env.py is not present and application
#   gets data directly from system-based variables
from os import path
if path.exists('env.py'):
    import env

# Defining application configruation information
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_DBNAME = os.getenv('DB_NAME')
    MONGO_URI = os.getenv('MONGO_URI')
    # Setting email parameters
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
