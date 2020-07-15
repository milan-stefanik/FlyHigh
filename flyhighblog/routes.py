# Importing required flask methods and functions
from flask import render_template, redirect, url_for, flash
# Importing variables from other application packages
from flyhighblog import app
from flyhighblog import mongo
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
    # If form is validated successfuly use Flask flash to render success
    #   message and redirect to index.html
    if form.validate_on_submit():
        flash('Account created for {} {}!'.format(form.firstname.data,
                                                  form.lastname.data),
              'success')
        return redirect(url_for('index'))
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
        if form.email.data == 'admin@flyhigh.com' and \
           form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. '
                  'Please check username and password.', 'danger')
    # Render login.html with respective login form
    return render_template('login.html', title='Login', form=form)
