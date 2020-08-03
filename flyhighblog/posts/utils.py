# Importing os to have access to sytem-based functions and variables
import os
# Importing required flask methods and functions
from flask import current_app
# Importing tool for Image processing
from PIL import Image
# Importing tool for generating secure random numbers
import secrets
# Importing variables from other application packages
from flyhighblog import mongo
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId


# Function for resizing and upload
#   of post pictures to database
def post_picture(form_picture_data):
    # Create random filename while keeping original file extension
    random_hex = secrets.token_hex(8)
    post_image = form_picture_data
    _, f_ext = os.path.splitext(post_image.filename)
    picture_fn = random_hex + f_ext

    # Set temporary path for post pictures
    picture_path = os.path.join(current_app.root_path,
                                'static/img/post-image',
                                picture_fn)

    # Resizing image - width 1000, aspect ratio kept
    basewidth = 1000
    i = Image.open(post_image)
    wpercent = (basewidth/float(i.size[0]))
    hsize = int((float(i.size[1])*float(wpercent)))
    i = i.resize((basewidth, hsize), Image.ANTIALIAS)

    # Saving resized image to temporary folder
    i.save(picture_path)

    # Open saved resized picture for read mode (r)
    #   with binary I/O (b)
    with open(picture_path, 'rb') as f:
        # Save resized picture to database
        mongo.save_file(picture_fn, f)

    # Delete resized picture from temporaty folder
    os.remove(picture_path)

    # Return picture filename
    return picture_fn


# Function for checking if user already inserted post picture in the past.
# If yes, delete the file from the database
def post_picture_check_and_delete(post):
    if 'picture' in post:
        image = mongo.db.fs.files.find_one(
                                           {'filename':
                                            post['picture']}
                                           )
        image_id = image['_id']
        # Deleting file from fs.files
        mongo.db.fs.files.delete_one({'_id': ObjectId(image_id)})
        # Deleting file from fs.chunks
        mongo.db.fs.chunks.delete_many({'files_id':
                                        ObjectId(image_id)})
