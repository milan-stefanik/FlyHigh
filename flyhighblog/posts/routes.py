# Importing functions for manipulating dates
from datetime import datetime
# Importing required flask methods and functions
from flask import (render_template, redirect, url_for, flash,
                   session, request, abort, Blueprint)
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
from bson.errors import InvalidId
# Importing variables from other application packages
from flyhighblog import mongo
from flyhighblog.posts.forms import PostForm, UpdatePostForm
from flyhighblog.posts.utils import (post_picture,
                                     post_picture_check_and_delete)


# Creating Blueprint object
posts = Blueprint('posts', __name__)


# Setting new variable to the context of templates - can be used in the base.html.
# users_all variable is used to generate list of authors for navbar
@posts.context_processor
def context_processor():
    # Users data is pulled from database and sorted by their first name
    users = mongo.db.users.find().sort('first_name')
    # Converting MongoDB object to list of dictionaries
    users = [dict(user) for user in users]
    return dict(users_all=users)


# Route for rendering New Post form; accessible only for 
#   registered and logged users
@posts.route('/post/new', methods=['GET', 'POST'])
def new_post():
    # If user is logged in (i.e. 'user_id' is in session),
    #  allow access to new post
    if 'user_id' in session:

        # Defining form variable - PostForm
        form = PostForm()

        # Check if form inputs are valid
        if form.validate_on_submit():
            
            # Resize and save picture to database
            picture_fn = post_picture(form.picture.data)

            # Save information from the form to database
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
            # Redirect to index.html
            return redirect(url_for('main.index'))

        # Render new_post.html
        return render_template('new_post.html', title='New Post', form=form)

    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        # Flash message informing user about the need to be logged in to be able
        #   to create a new post.
        flash('Please login to access this page.', 'info')
        # Redirect to log-in page
        return redirect(url_for('users.login', next=request.endpoint))


# Route for displaying post; accessible also for non-registered users
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

    # Rendering post.html
    return render_template('post.html', title=post['title'], post=post)


# Route for rendering Update Post form; accessible only for 
#   registered and logged users
# Post can be updated only by its author
@posts.route('/post/<post_id>/update',  methods=['GET', 'POST'])
def update_post(post_id):
    # If user is logged in (i.e. 'user_id' is in session),
    #  allow access to update post
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

        # Defining form variable - UpdatePostForm
        form = UpdatePostForm()

        # Check if form inputs are valid
        if form.validate_on_submit():

            # Checking if there are picture data in the form
            if form.picture.data:

                # Checking if user already inserted post picture in the past.
                # If yes, delete the old file from the database
                post_picture_check_and_delete(post)

                # Resize and save picture to database
                picture_fn = post_picture(form.picture.data)

                # Save file name reference to post document
                posts.update({'_id': ObjectId(post_id)},
                             {'$set': {
                                        'picture': picture_fn,
                                      }
                              })

            # Update only those post details that have been changed
            # All other details shall remain same
            posts.update({'_id': ObjectId(post_id)},
                         {'$set': {
                                    'title': form.title.data,
                                    'content': form.content.data,
                                  }
                          })

            # Generate flash message on successful post update
            flash('Post has been updated!', 'success')

            # Redirect to updated post
            return redirect(url_for('posts.post', post_id=post_id))

        # Pull data from database and insert them to post update form
        elif request.method == 'GET':
            form.title.data = post['title']
            form.content.data = post['content']
        return render_template('update_post.html', title='Update Post',
                               form=form, post_id=post_id)

    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        # Flash message informing user about the need to be logged in to be able
        #   to update existing post.
        flash('Please login to access this page.', 'info')
        # Redirect to login page
        return redirect(url_for('users.login', next=request.endpoint))


# Route for deleting post ; accessible only for 
#   registered and logged users
# Post can be deleted only by its author
@posts.route("/post/<post_id>/delete", methods=['POST'])
def delete_post(post_id):
    # If user is logged in (i.e. 'user_id' is in session),
    #  allow post delete
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

        # Checking if user already inserted post picture in the past.
        # If yes, delete the old file from the database
        post_picture_check_and_delete(post)

        # Delete post from database
        mongo.db.posts.delete_one({'_id': ObjectId(post_id)})

        # Flash message informing user that the post was deleted
        flash('Post has been deleted.', 'success')
        
        # Redirect to index.html
        return redirect(url_for('main.index'))
    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        # Flash message informing user about the need to be logged in to be able
        #   to delete post.
        flash('Please login to access this page.', 'info')
        # Redirect to login page
        return redirect(url_for('users.login', next=request.endpoint))
