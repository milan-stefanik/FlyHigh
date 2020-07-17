# Importing required flask methods and functions
from flask import render_template, redirect, url_for, flash
# Importing flask_login tools and methods
from flask_login import login_user, current_user, logout_user, login_required
# Importing variables from other application packages
from flyhighblog import app
from flyhighblog import mongo
from flyhighblog import bcrypt
from flyhighblog import login_manager

from flyhighblog.forms import RegistrationForm, LoginForm


# Index route - listing all posts
@app.route('/')
@app.route('/index')
def index():
    # Rendering index.html template with list of all posts pulled from MongoDB
    return render_template('index.html', posts=mongo.db.posts.find())


# About route
@app.route('/about')
def about():
    # Rendering about.html template with variable amending web-page title
    return render_template('about.html', title='About')


# Register route - form for registration of new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Defining form variable - Registration form
    form = RegistrationForm()
    # If form is validated successfuly, hash password,
    #   save userdata to database
    #   and use Flask flash to render success
    #   message and redirect to index.html
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user_doc = {
                    'first_name': form.firstname.data,
                    'last_name': form.lastname.data,
                    'username': form.username.data,
                    'email': form.email.data,
                    'password': hashed_password,
                    }
        mongo.db.users.insert_one(user_doc)
        flash('Account has been created! You can now log in.',
              'success')
        return redirect(url_for('login'))
    # Render register.html with respective registration form
    return render_template('register.html', title='Register', form=form)


# Login route - form for user login and authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Defining form variable - Login form
    form = LoginForm()
    # Validate passed login information,
    #   use Flask flash to render respective message (passed/failed)
    #   and redirect to index.html
    if form.validate_on_submit():
        user = mongo.db.users.find({'email': form.email.data})
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            flash('Login Unsuccessful. '
                  'Please check username and password.', 'danger')
    # Render login.html with respective login form
    return render_template('login.html', title='Login', form=form)
