# Importing os to have access to sytem-based functions and variables
import os
# Importing tool for generating secure random numbers
import secrets
# Importing required flask methods and functions
from flask import render_template, redirect, url_for, flash, session, request
# Importing Werkzeug Security Functions
from werkzeug.security import generate_password_hash, check_password_hash
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
# Importing variables from other application packages
from flyhighblog import app, mongo
from flyhighblog.forms import RegistrationForm, LoginForm, UpdateAccountForm


# Index route - listing all posts
@app.route('/')
@app.route('/index')
def index():
    # Rendering index.html template with list of all posts pulled from MongoDB
    # 'title' variable customizes web-page title
    return render_template('index.html', posts=mongo.db.posts.find(),
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
                    # Deleting file from fs.chungs
                    mongo.db.fs.chunks.delete_many({'files_id':
                                                    ObjectId(image_id)})
                # Create random filename while keeping original file extension
                random_hex = secrets.token_hex(8)
                profile_image = form.picture.data
                _, f_ext = os.path.splitext(profile_image.filename)
                picture_fn = random_hex + f_ext
                # Save file to the database
                mongo.save_file(picture_fn, profile_image)
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
