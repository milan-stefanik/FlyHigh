# Importing os to have access to sytem-based functions and variables
import os
# Importing required flask methods and functions
from flask import url_for, current_app
# Importing tool for generating secure random numbers
import secrets
# Importing tool for Image processing
from PIL import Image
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


# Function for resizing and upload
#   of profile_images to database
def profile_image(form_picture_data):
    # Create random filename while keeping original file extension
    random_hex = secrets.token_hex(8)
    profile_image = form_picture_data
    _, f_ext = os.path.splitext(profile_image.filename)
    picture_fn = random_hex + f_ext

    # Set temporary path for profile pictures
    picture_path = os.path.join(current_app.root_path,
                                'static/img/profile-image',
                                picture_fn)

    # Resizing image
    output_size = (125, 125)
    i = Image.open(profile_image)
    i.thumbnail(output_size)

    # Saving resized image to temporary folder
    i.save(picture_path)

    # Open saved resized picture for read mode (r)
    #   with binary I/O (b)
    with open(picture_path, 'rb') as f:
        # Save resized picture to database
        mongo.save_file(picture_fn, f)

    # Delete resized picture from temporaty folder
    os.remove(picture_path)

    return picture_fn


# Function for checking if user already inserted profile image in the past.
# If yes, delete the file from the database
def profile_image_check_and_delete(user):
    if 'profile_img' in user:
        image = mongo.db.fs.files.find_one(
                                           {'filename':
                                            user['profile_img']}
                                           )
        image_id = image['_id']
        # Deleting file from fs.files
        mongo.db.fs.files.delete_one({'_id': ObjectId(image_id)})
        # Deleting file from fs.chunks
        mongo.db.fs.chunks.delete_many({'files_id':
                                        ObjectId(image_id)})
