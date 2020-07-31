# Importing form validation and rendering library integrated in Flask
from flask_wtf import FlaskForm
# Importing form file input field
from flask_wtf.file import FileField, FileAllowed
# Importing required field types
from wtforms import (StringField, PasswordField,
                     SubmitField, TextAreaField)
# Importing field validators
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)
# Importing mongo for validating duplicated username/email during registration
from flyhighblog import mongo
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
# Importing required flask methods and functions
from flask import session


# Defining form for registration of users including form validation parameters
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=25)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail',
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
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')


# Defining form for changing user information
#   including form validation parameters
class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=25)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    # Validation of username - if exists, return validation error
    def validate_username(self, username):
        user = mongo.db.users.find_one({'_id':  ObjectId(session['user_id'])})
        if username.data != user['username']:
            if mongo.db.users.count_documents({'username': username.data},
                                              limit=1):
                raise ValidationError(
                    'Username already exists. Please choose different one.')

    # Validation of email - if exists, return validation error
    def validate_email(self, email):
        user = mongo.db.users.find_one({'_id':  ObjectId(session['user_id'])})
        if email.data != user['email']:
            if mongo.db.users.count_documents({'email': email.data}, limit=1):
                raise ValidationError(
                    'Account with this e-mail address is already registered. '
                    'Please log in or create an account with different'
                    'e-mail address.')


# Defining form for creating new post
#   including form validation parameters
class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload post picture',
                        validators=[DataRequired(),
                                    FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')


# Defining form for updating existing post
#   including form validation parameters
class UpdatePostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Change post picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')


# Defining form for requesting password reset
#   including form validation parameters
class RequestPasswordResetForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')

    # Validation of email - if does not exist, return validation error
    def validate_email(self, email):
        if mongo.db.users.count_documents({'email': email.data}, limit=1) < 1:
            raise ValidationError(
                                  'There is no account associated '
                                  'with this e-mail address! '
                                  'You must register first.')


# Defining form for password change
#   including form validation parameters
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset Password')
