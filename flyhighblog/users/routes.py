# Importing required flask methods and functions
from flask import (render_template, redirect, url_for, flash, session, request,
                   Blueprint)
# Importing Flask pagination function
from flask_paginate import Pagination
# Importing Werkzeug Security Functions
from werkzeug.security import generate_password_hash, check_password_hash
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
# Importing variables from other application packages
from flyhighblog import mongo
from flyhighblog.users.forms import (RegistrationForm, LoginForm,
                                     UpdateAccountForm,
                                     RequestPasswordResetForm,
                                     PasswordResetForm)
from flyhighblog.users.utils import (verify_reset_token,
                                     send_email,
                                     profile_image,
                                     profile_image_check_and_delete)
from flyhighblog.main.utils import get_items


# Creating Blueprint object
users = Blueprint('users', __name__)


# Setting new variable to the context of templates - can be used
#   in the base.html.
# users_all variable is used to generate list of authors for navbar
@users.context_processor
def context_processor():
    # Users data is pulled from database and sorted by their first name
    users = mongo.db.users.find().sort('first_name')
    # Converting MongoDB object to list of dictionaries
    users = [dict(user) for user in users]
    return dict(users_all=users)


# Register route - form for registration of new users
@users.route('/register', methods=['GET', 'POST'])
def register():
    # Checking if user is logged in
    if 'user_id' in session:
        # If user logged in, redirect to index.html
        return redirect(url_for('main.index'))

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
        return redirect(url_for('users.login'))

    # Render register.html with respective registration form
    # 'title' variable customizes web-page title
    return render_template('register.html', title='Register', form=form)


# Login route - form for user login and authentication
@users.route('/login', methods=['GET', 'POST'])
def login():
    # Checking if user is logged in.
    if 'user_id' in session:
        # If user logged in, redirect to index.html
        return redirect(url_for('main.index'))

    # Defining form variable - Login form
    form = LoginForm()

    # Validate passed login information,
    #   use Flask flash to render respective message
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
                return redirect(url_for('main.index'))

        else:
            # Defining flash message for failed login
            flash('Login Unsuccessful. Please check email and password.',
                  'danger')

    # Render login.html with respective login form
    # 'title' variable customizes web-page title
    return render_template('login.html', title='Login', form=form)


# Logout route
@users.route("/logout")
def logout():
    # Removing 'user_id' from session
    session.pop('user_id', None)
    # Defining flash message for logout
    flash('You have been logged out.', 'info')
    # Redirecting to index.html
    return redirect(url_for('main.index'))


# Route for editing user's info; accessible only for registered and
#   logged users, user can edit only own account information
@users.route("/account", methods=['GET', 'POST'])
def account():
    # If user is logged in (i.e. 'user_id' is in session),
    #  allow access to account.html and display corresponding
    #  account information
    if 'user_id' in session:

        # Defining form variable - UpdateAccountForm
        form = UpdateAccountForm()
        user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
        users = mongo.db.users

        # Check if form inputs are valid
        if form.validate_on_submit():

            # Checking if there are picture data in the form
            if form.picture.data:

                # Checking if user already set profile image in the past.
                # If yes, delete the old file from the database
                profile_image_check_and_delete(user)

                # Resize and save picture to database
                picture_fn = profile_image(form.picture.data)

                # Save file name reference to user document
                users.update({'_id': ObjectId(session['user_id'])},
                             {'$set': {
                                        'profile_img': picture_fn,
                             }
                             })

            # Update only those user details that have been changed
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
            return redirect(url_for('users.account'))

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
        # Flash message informing user about the need to be logged in
        #   to be able to edit account information.
        flash('Please login to access this page.', 'info')
        # Redirect to log-in page
        return redirect(url_for('users.login', next=request.endpoint))


# Route for displaying posts written by particular users
@users.route('/user/<string:username>')
def user_posts(username):
    # Filtering posts saved in database by username
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


# Route for requesting password reset
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # Checking if user is logged in.
    if 'user_id' in session:
        # If user logged in, redirect to index.html
        return redirect(url_for('main.index'))

    # Defining form variable - RequestPasswordResetForm
    form = RequestPasswordResetForm()

    # Check if form inputs are valid
    if form.validate_on_submit():
        # Find user by e-mail address
        user = mongo.db.users.find_one({'email': form.email.data})
        # Send password reset instructions to user's e-mail
        send_email(user)
        # Flash message informing that e-mail with password reset instructions
        #   has been sent.
        flash('An e-mail with password reset instructions has been sent.',
              'info')
        # Redirect to log-in page
        return redirect(url_for('users.login'))
    # Render password reset request form
    return render_template('reset_request.html',
                           title='Reset Password', form=form)


# Route for reseting password; accessed via link sent to user by e-mail
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    # Checking if user is logged in.
    if 'user_id' in session:
        # If user logged in, redirect to index.html
        return redirect(url_for('main.index'))

    # Verify, if token in the link is valid
    user = verify_reset_token(token)
    if user is None:
        flash('Token is invalid or expired!', 'warning')
        # If the token is invalid, redirect to request password reset page
        return redirect(url_for('users.reset_request'))

    user_id = str(user['_id'])
    users = mongo.db.users

    # Defining form variable - PasswordResetForm
    form = PasswordResetForm()

    # Check if form inputs are valid
    if form.validate_on_submit():

        # Hashing the password
        hashpass = generate_password_hash(form.password.data)

        # Update password data in the database
        users.update({'_id': ObjectId(user_id)},
                     {'$set': {
                               'password': hashpass,
                              }
                      })

        # Flash message informing that password has been changed.
        flash('Your password has been updated! You are now able to log in',
              'success')

        # Redirect to login page
        return redirect(url_for('users.login'))

    # Render password reset page
    return render_template('reset_password.html',
                           title='Reset Password', form=form)
