# Importing form validation and rendering library integrated fo Flask
from flask_wtf import FlaskForm
# Importing required field types
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# Importing field validators
from wtforms.validators import DataRequired, Length, Email, EqualTo


# Defining form for registration of users including form validation parameters
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=25)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')


# Defining form for user login including from validation parameters
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
