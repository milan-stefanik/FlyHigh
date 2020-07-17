# Importing form validation and rendering library integrated fo Flask
from flask_wtf import FlaskForm
# Importing required field types
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# Importing field validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# Importing mongo for validating duplicated username/email during registration
from flyhighblog import mongo


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

    # Validation of username - if exists, return validation error
    def validate_username(self, username):
        if mongo.db.users.count_documents({'username': username.data},
                                          limit=1):
            raise ValidationError(
                'Username already exists. Please choose different one.')

    # Validation of email - if exists, return validation error
    def validate_email(self, email):
        if mongo.db.users.count_documents({'email': email.data}, limit=1):
            raise ValidationError(
                'Account with this e-mail address is already registered. '
                'Please log in or create an account with different'
                'e-mail address.')


# Defining form for user login including from validation parameters
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
