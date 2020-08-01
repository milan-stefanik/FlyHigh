# Importing os to have access to sytem-based functions and variables
import os
# Importing tool for generating secure random numbers
import secrets
from datetime import datetime
# Importing tool for Image processing
from PIL import Image
# Importing required flask methods and functions
from flask import (render_template, redirect, url_for, flash,
                   session, request, abort, Blueprint, current_app)
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
from bson.errors import InvalidId
# Importing variables from other application packages
from flyhighblog import mongo
from flyhighblog.posts.forms import PostForm, UpdatePostForm


posts = Blueprint('posts', __name__)


@posts.context_processor
def context_processor():
    users = mongo.db.users.find().sort('first_name')
    # Converting MongoDB object to list of dictionaries
    users = [dict(user) for user in users]
    return dict(users_all=users)


@posts.route('/post/new', methods=['GET', 'POST'])
def new_post():
    # If user is logged in (i.e. 'user_id' is in session),
    #  allow access to new post
    if 'user_id' in session:

        # Defining form variable - UpdateAccountForm
        form = PostForm()

        # Check if form inputs are valid
        if form.validate_on_submit():
            # Create random filename while keeping original file extension
            random_hex = secrets.token_hex(8)
            post_image = form.picture.data
            _, f_ext = os.path.splitext(post_image.filename)
            picture_fn = random_hex + f_ext

            # Set temporary path for post pictures
            picture_path = os.path.join(current_app.root_path,
                                        'static/img/post-image',
                                        picture_fn)

            # Resizing image
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

            # Save file name reference to post document
            post_doc = {
                    'title': form.title.data,
                    'date_posted': datetime.utcnow(),
                    'content': form.content.data,
                    'author': session['user_id'],
                    'picture': picture_fn,
                    }
            mongo.db.posts.insert_one(post_doc)

            # Flash message informing about successful creation of post
            flash('Your post has been created!', 'success')
            return redirect(url_for('main.index'))

        return render_template('new_post.html', title='New Post', form=form)

    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        flash('Please login to access this page.', 'info')
        return redirect(url_for('users.login', next=request.endpoint))


@posts.route('/post/<post_id>')
def post(post_id):
    # Check validity of ObjectId and return 404 if invalid
    try:
        ObjectId(post_id)
    except (InvalidId, TypeError):
        abort(404)
    post = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})

    # If post does not exist retutn 404
    if post is None:
        abort(404)

    # Converting MongoDB object to dictionary
    post = dict(post)
    user = mongo.db.users.find_one({'_id': ObjectId(post['author'])})

    # Amending post dictionary so as it contains required user
    #   specific data
    post['first_name'] = user['first_name'].title()
    post['last_name'] = user['last_name'].title()
    post['profile_image'] = user['profile_img']

    return render_template('post.html', title=post['title'], post=post)


@posts.route('/post/<post_id>/update',  methods=['GET', 'POST'])
def update_post(post_id):
    # If user is logged in (i.e. 'user_id' is in session),
    #  allow access to new post
    if 'user_id' in session:

        # Check validity of ObjectId and return 404 if invalid
        try:
            ObjectId(post_id)
        except (InvalidId, TypeError):
            abort(404)

        posts = mongo.db.posts
        post = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})

        # If post does not exist retutn 404
        if post is None:
            abort(404)

        # If logged user is not author of post, return 403
        if post['author'] != session['user_id']:
            abort(403)

        form = UpdatePostForm()

        if form.validate_on_submit():

            # Checking if there are picture data in the form
            if form.picture.data:

                # Checking if user already inserted post picture in the past.
                # If yes, delete the old file from the database
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

                # Create random filename while keeping original file
                #   extension
                random_hex = secrets.token_hex(8)
                post_image = form.picture.data
                _, f_ext = os.path.splitext(post_image.filename)
                picture_fn = random_hex + f_ext

                # Set temporary path for post pictures
                picture_path = os.path.join(current_app.root_path,
                                            'static/img/post-image',
                                            picture_fn)

                # Resizing image
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

                # Save file name reference to post document
                posts.update({'_id': ObjectId(post_id)},
                             {'$set': {
                                        'picture': picture_fn,
                                      }
                              })

            # Update only those used details that have been changed
            # All other details shall remain same
            posts.update({'_id': ObjectId(post_id)},
                         {'$set': {
                                    'title': form.title.data,
                                    'content': form.content.data,
                                  }
                          })

            # Generate flash message on user info update
            flash('Post has been updated!', 'success')

            # Redirect to account.html
            return redirect(url_for('posts.post', post_id=post_id))

        # Pull data from database and insert them to account form
        # Pull data from database and insert them to update post form
        elif request.method == 'GET':
            form.title.data = post['title']
            form.content.data = post['content']
        return render_template('update_post.html', title='Update Post',
                               form=form)

    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        flash('Please login to access this page.', 'info')
        return redirect(url_for('users.login', next=request.endpoint))


# Route for deleting post
@posts.route("/post/<post_id>/delete", methods=['POST'])
def delete_post(post_id):
    # If user is logged in (i.e. 'user_id' is in session),
    #  allow access to new post
    if 'user_id' in session:

        # Check validity of ObjectId and return 404 if invalid
        try:
            ObjectId(post_id)
        except (InvalidId, TypeError):
            abort(404)
        post = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})

        # If post does not exist retutn 404
        if post is None:
            abort(404)

        # If logged user is not author of post, return 403
        if post['author'] != session['user_id']:
            abort(403)

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

        # Delete post from database
        mongo.db.posts.delete_one({'_id': ObjectId(post_id)})

        flash('Post has been deleted.', 'success')
        return redirect(url_for('main.index'))
    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        flash('Please login to access this page.', 'info')
        return redirect(url_for('users.login', next=request.endpoint))
