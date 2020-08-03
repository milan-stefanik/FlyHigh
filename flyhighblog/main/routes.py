# Importing required flask methods and functions
from flask import render_template, request, Blueprint
# Importing Flask pagination function
from flask_paginate import Pagination
# Importing Tools for working with MongoDB ObjectIds
from bson.objectid import ObjectId
# Importing variables from other application packages
from flyhighblog import mongo
from flyhighblog.main.utils import get_items


# Creating Blueprint object
main = Blueprint('main', __name__)


# Setting new variable to the context of templates - and can be used
#   in the base.html.
# users_all variable is used to generate list of authors for navbar
@main.context_processor
def context_processor():
    # Users data is pulled from database and sorted by their first name
    users = mongo.db.users.find().sort('first_name')
    # Converting MongoDB object to list of dictionaries
    users = [dict(user) for user in users]
    return dict(users_all=users)


# Index route - listing all posts
@main.route('/')
@main.route('/index')
def index():
    # Posts data is pulled from database and sorted by date in descending
    #   order
    posts = mongo.db.posts.find().sort('date_posted', -1)

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
    return render_template('index.html',
                           posts=pagination_posts,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           title='Home')


# Retrieve file from database based on filename
@main.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)
