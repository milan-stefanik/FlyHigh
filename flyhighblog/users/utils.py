# Importing required flask methods and functions
from flask import url_for, current_app
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
# Importing Serializer for Password reset
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# Importing flask_mail message
from flask_mail import Message
# Importing variables from other application packages
from flyhighblog import mongo, mail


# Function for generating password reset token
def get_reset_token(user, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': str(user['_id'])}).decode('utf-8')


# Function for verifying token
def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return mongo.db.users.find_one({'_id': ObjectId(user_id)})


# Function for sending password reset email
def send_email(user):
    token = get_reset_token(user)
    msg = Message('Password Reset Request',
                  sender='noreply@flyhigh.com',
                  recipients=[user['email']])
    msg.body = '''
               To reset your password, visit the following link:
               {}
               If you did not make this request then simply ignore
               this email and no changes will be made.
               '''.format(url_for('users.reset_password',
                                  token=token, _external=True))
    mail.send(msg)
