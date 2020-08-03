# Importing required flask methods and functions
from flask import Blueprint, render_template


# Creating Blueprint object
errors = Blueprint('errors', __name__)


# 404 error page route
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='404 error'), 404


# 403 error page route
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html',  title='403 error'), 403


# 500 error page route
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html',  title='500 error'), 500
