# Importing os to have access to sytem-based functions and variables
import os
# Importing tool for generating secure random numbers
import secrets
from datetime import datetime
# Importing tool for Image processing
from PIL import Image
# Importing required flask methods and functions
from flask import (render_template, redirect, url_for, flash,
                   session, request, abort)
# Importing Flask pagination function
from flask_paginate import Pagination
# Importing Werkzeug Security Functions
from werkzeug.security import generate_password_hash, check_password_hash
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
from bson.errors import InvalidId
# Importing Serializer for Password reset
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# Importing flask_mail message
from flask_mail import Message
# Importing variables from other application packages
from flyhighblog import app, mongo, mail
from flyhighblog.forms import (RegistrationForm, LoginForm,
                               UpdateAccountForm, PostForm,
                               UpdatePostForm, RequestPasswordResetForm,
                               PasswordResetForm)


@app.context_processor
def context_processor():
    users = mongo.db.users.find().sort('first_name')
    # Converting MongoDB object to list of dictionaries
    users = [dict(user) for user in users]
    return dict(users_all=users)


# Function to filter by pagination parameters
def get_items(items, offset, per_page):
    return items[offset: offset + per_page]


# Index route - listing all posts
@app.route('/')
@app.route('/index')
def index():
    posts = mongo.db.posts.find().sort('date_posted', -1)

    # Converting MongoDB object to list of dictionaries
    posts = [dict(post) for post in posts]

    # Amending list of dictionaries so as it contains required user
    #   specific data
    for post in posts:
        user = mongo.db.users.find_one({'_id': ObjectId(post['author'])})
        post['first_name'] = user['first_name'].title()
        post['last_name'] = user['last_name'].title()
        post['username'] = user['username']

    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    total = len(posts)

    pagination_posts = get_items(posts, offset=offset, per_page=per_page)

    # Pagination options - refer to https://pythonhosted.org/Flask-paginate/
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4', inner_window=1,
                            outer_window=0)

    # Rendering index.html template with list of all posts pulled from MongoDB
    # 'title' variable customizes web-page title
    return render_template('index.html',
                           posts=pagination_posts,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           title='Home')


# About route
@app.route('/about')
def about():
    # Rendering about.html template
    # 'title' variable customizes web-page title
    return render_template('about.html', title='About')


# Register route - form for registration of new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Checking if user is logged in
    if 'user_id' in session:
        # If user logged in, redirect to index.html
        return redirect(url_for('index'))

    # Defining form variable - Registration form
    form = RegistrationForm()

    # If form is validated successfuly, hash password,
    #   save userdata to database
    #   and use Flask flash to render success
    #   message and redirect to index.html
    if form.validate_on_submit():

        # Hashing the password
        hashpass = generate_password_hash(form.password.data)

        # Saving data from form to variable
        user_doc = {
                    'first_name': form.firstname.data.lower(),
                    'last_name': form.lastname.data.lower(),
                    'username': form.username.data,
                    'email': form.email.data.lower(),
                    'password': hashpass,
                    }
        # Sending data to database
        mongo.db.users.insert_one(user_doc)

        # Defining flash message for successful registration
        flash('Account has been created! You can now log in.',
              'success')

        # Redirecting to login.html
        return redirect(url_for('login'))

    # Render register.html with respective registration form
    # 'title' variable customizes web-page title
    return render_template('register.html', title='Register', form=form)


# Login route - form for user login and authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Checking if user is logged in.
    if 'user_id' in session:
        # If user logged in, redirect to index.html
        return redirect(url_for('index'))

    # Defining form variable - Login form
    form = LoginForm()

    # Validate passed login information,
    #   use Flask flash to render respective message (passed/failed)
    #   and redirect to index.html
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'email': form.email.data.lower()})

        # Checking if provided password corresponds to password saved in
        #   database
        if user and check_password_hash(user['password'],
                                        form.password.data):
            # Saving 'user_id' into session cookie
            session['user_id'] = str(user['_id'])

            # Defining flash message for successful login
            flash('You are now logged in as {} '
                  '{}'.format(user['first_name'].title(),
                              user['last_name'].title()),
                  'success')

            # Getting information about user's intention before
            #   login page was displayed
            next_page = request.args.get('next')

            # After login, redirecting to page user as per the
            #   user's original intention
            if next_page:
                return redirect(url_for(next_page))
            else:
                return redirect(url_for('index'))

        else:
            # Defining flash message for failed login
            flash('Login Unsuccessful. Please check email and password.',
                  'danger')

    # Render login.html with respective login form
    # 'title' variable customizes web-page title
    return render_template('login.html', title='Login', form=form)


# Logout route
@app.route("/logout")
def logout():
    # Removing 'user_id' from session
    session.pop('user_id', None)
    # Defining flash message for logout
    flash('You have been logged out.', 'info')
    # Redirecting to index.html
    return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
def account():
    # If user is logged in (i.e. 'user_id' is in session),
    #  allow access to account.html and display corresponding
    #  account information
    if 'user_id' in session:

        # Defining form variable - UpdateAccountForm
        form = UpdateAccountForm()
        user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
        users = mongo.db.users
        if form.validate_on_submit():

            # Checking if there are picture data in the form
            if form.picture.data:

                # Checking if user already set profile image in the past.
                # If yes, delete the old file from the database
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

                # Create random filename while keeping original file extension
                random_hex = secrets.token_hex(8)
                profile_image = form.picture.data
                _, f_ext = os.path.splitext(profile_image.filename)
                picture_fn = random_hex + f_ext

                # Set temporary path for profile pictures
                picture_path = os.path.join(app.root_path,
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

                # Save file name reference to user document
                users.update({'_id': ObjectId(session['user_id'])},
                             {'$set': {
                                        'profile_img': picture_fn,
                             }
                             })

            # Update only those used details that have been changed
            # All other details shall remain same
            users.update({'_id': ObjectId(session['user_id'])},
                         {'$set': {
                                    'first_name': form.firstname.data.lower(),
                                    'last_name': form.lastname.data.lower(),
                                    'username': form.username.data,
                                    'email': form.email.data.lower(),
                                   }
                          })

            # Generate flash message on user info update
            flash('Your account has been updated!', 'success')
            # Redirect to account.html
            return redirect(url_for('account'))

        # Pull data from database and insert them to account form
        elif request.method == 'GET':
            form.firstname.data = user['first_name'].title()
            form.lastname.data = user['last_name'].title()
            form.username.data = user['username']
            form.email.data = user['email']

        # Render account.html template with respective user info
        return render_template('account.html', title='Account',
                               user=user, form=form)

    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        flash('Please login to access this page.', 'info')
        return redirect(url_for('login', next=request.endpoint))


# Retrieve file from database based on filename
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/post/new', methods=['GET', 'POST'])
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
            picture_path = os.path.join(app.root_path,
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
            return redirect(url_for('index'))

        return render_template('new_post.html', title='New Post', form=form)

    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        flash('Please login to access this page.', 'info')
        return redirect(url_for('login', next=request.endpoint))


@app.route('/post/<post_id>')
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


@app.route('/post/<post_id>/update',  methods=['GET', 'POST'])
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
                picture_path = os.path.join(app.root_path,
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
            return redirect(url_for('post', post_id=post_id))

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
        return redirect(url_for('login', next=request.endpoint))


# Route for deleting post
@app.route("/post/<post_id>/delete", methods=['POST'])
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
        return redirect(url_for('index'))
    # If user is not logged in, redirect to login.html and save info about
    #   user's intention so as the corresponding page can be displayed after
    #   successful login.
    else:
        flash('Please login to access this page.', 'info')
        return redirect(url_for('login', next=request.endpoint))


# Route for displaying posts written by particular users
@app.route('/user/<string:username>')
def user_posts(username):
    user = mongo.db.users.find_one({'username': username})
    user_id = str(user['_id'])
    first_name = user['first_name'].title()
    last_name = user['last_name'].title()
    posts = mongo.db.posts.find({'author': user_id}).sort('date_posted', -1)

    # Converting MongoDB object to list of dictionaries
    posts = [dict(post) for post in posts]

    # Amending list of dictionaries so as it contains required user
    #   specific data
    for post in posts:
        user = mongo.db.users.find_one({'_id': ObjectId(post['author'])})
        post['first_name'] = user['first_name'].title()
        post['last_name'] = user['last_name'].title()
        post['username'] = user['username']

    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    total = len(posts)

    pagination_posts = get_items(posts, offset=offset, per_page=per_page)

    # Pagination options - refer to https://pythonhosted.org/Flask-paginate/
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4', inner_window=1,
                            outer_window=0)

    # Rendering index.html template with list of all posts pulled from MongoDB
    # 'title' variable customizes web-page title
    return render_template('user_posts.html',
                           first_name=first_name,
                           last_name=last_name,
                           posts=pagination_posts,
                           posts_count=total,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           title='User Posts')


# Function for generating password reset token
def get_reset_token(user, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': str(user['_id'])}).decode('utf-8')


# Function for verifying token
def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
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
               To reset your password, visit the following link: {}
               If you did not make this request then simply ignore
               this email and no changes will be made.
               '''.format(url_for('reset_password',
                                  token=token, _external=True))
    mail.send(msg)


# Route for requesting password reset
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # Checking if user is logged in.
    if 'user_id' in session:
        # If user logged in, redirect to index.html
        return redirect(url_for('index'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'email': form.email.data})
        send_email(user)
        flash('An e-mail with password reset instructions has been sent.',
              'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',
                           title='Reset Password', form=form)


# Route for reseting password
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    # Checking if user is logged in.
    if 'user_id' in session:
        # If user logged in, redirect to index.html
        return redirect(url_for('index'))
    user = verify_reset_token(token)
    user_id = str(user['_id'])
    users = mongo.db.users
    if user_id is None:
        flash('Token is invalid or expired!', 'warning')
        return redirect(url_for('reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashpass = generate_password_hash(form.password.data)
        # Save file name reference to user document
        users.update({'_id': ObjectId(user_id)},
                     {'$set': {
                               'password': hashpass,
                              }
                     })
        flash('Your password has been updated! You are now able to log in',
              'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html',
                           title='Reset Password', form=form)
