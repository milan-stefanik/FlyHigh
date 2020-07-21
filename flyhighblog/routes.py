# Importing required flask methods and functions
from flask import render_template, redirect, url_for, flash, session, request
# Importing Werkzeug Security Functions
from werkzeug.security import generate_password_hash, check_password_hash
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
# Importing variables from other application packages
from flyhighblog import app, mongo
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
    # Checking if user is logged in
    if 'user_id' in session:
        return redirect(url_for('index'))
    # Defining form variable - Registration form
    form = RegistrationForm()
    # If form is validated successfuly, hash password,
    #   save userdata to database
    #   and use Flask flash to render success
    #   message and redirect to index.html
    if form.validate_on_submit():
        hashpass = generate_password_hash(form.password.data)
        user_doc = {
                    'first_name': form.firstname.data.lower(),
                    'last_name': form.lastname.data.lower(),
                    'username': form.username.data.lower(),
                    'email': form.email.data.lower(),
                    'password': hashpass,
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
    # Checking if user is logged in
    if 'user_id' in session:
        return redirect(url_for('index'))
    # Defining form variable - Login form
    form = LoginForm()
    # Validate passed login information,
    #   use Flask flash to render respective message (passed/failed)
    #   and redirect to index.html
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'email': form.email.data.lower()})
        if user and check_password_hash(user['password'],
                                        form.password.data):
            session['user_id'] = str(user['_id'])
            flash('You are now logged in as {} '
                  '{}'.format(user['first_name'].title(),
                              user['last_name'].title()),
                  'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(url_for(next_page))
            else:
                return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password.',
                  'danger')
    # Render login.html with respective login form
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route("/account")
def account():
    if 'user_id' in session:
        user = mongo.db.users.find_one({'_id':  ObjectId(session['user_id'])})
        return render_template('account.html', title='Account',
                               user=user)
    else:
        flash('Please login to access this page.', 'info')
        return redirect(url_for('login', next=request.endpoint))
