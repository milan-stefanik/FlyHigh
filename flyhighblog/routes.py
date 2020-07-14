from flask import render_template, redirect, url_for, flash
from flyhighblog import app
from flyhighblog import mongo
from flyhighblog.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', posts=mongo.db.posts.find())


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {} {}!'.format(form.firstname.data,
                                                  form.lastname.data),
              'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@flyhigh.com' and \
           form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. '
                  'Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)
