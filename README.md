# FlyHigh Blog: Bloggig application for aviation professionals and enthusiasts
Code Institute - Third Milestone Project: Data Centric Development

The blogging application was developed for authors wanting to share their opinions and experience from the field of civil aviation, and for the readers craving for the latest aviation news.

## Demo
A live demo of the website has been developed  [here](http://fly-high-blog.herokuapp.com/).

![Responsive Web Demo](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/demo.gif "Responsive Web Demo")


Responsive Web Demo GIF image was recorded using [Am I Responsive?](http://ami.responsivedesign.is) website. 

## UX

### User stories

#### Non-registered user
* User can access home page with a list of published posts.
* User can read published posts.
* User can filter posts by author (either through links in navigation bar or by clicking on post's author name).
* User can register and thus become a registered user (either trhough a link in navigation bar or by means of Login page).
* User is not allowed to access restricted area of the website (i.e. edit user account information or create, update or delete posts).
* User cannot reset password (in an attempt to do so, user will be asked to register).
* When trying to access restricted area, user is redirected to Login page.

#### Registered but unauthenticated user
* User can access home page with a list of published posts.
* User can read published posts.
* User can filter posts by author (either through links in navigation bar or by clicking on post's author name).
* User cannot register (registration will be rejected if existing e-mail address or username is passed through the registration form).
* User can log in and thus become authenticated user.
* User is not allowed to access restricted area of the website (i.e. edit user account information or create, update or delete posts).
* User can request password change and if correct user information is passed through the respective form, user will receive password reset instructions via e-mail.
* Using a password reset link received via e-mail, user can reset/change password. 
* When trying to access restricted area, user is redirected to Login page.

#### Registered and authenticated user
* User can access home page with a list of published posts.
* User can read published posts
* User can filter posts by author (either through links in navigation bar or by clicking on post's author name).
* User cannot register (in an attempt to open registration form, authenticated user is redirected to home page).
* User cannot log in (in an attempt to open registration form, authenticated user is redirected to home page).
* User can logout and thus become registerd but unauthenticated user.
* User can update own user information and change own profile image.
* User cannot update user information and change profile image of other users.
* User cannot request password reset (in an attempt to do so, user would be redirected to home page).
* User can create new post.
* User can update and delete own posts.
* User cannot update and delete posts of other users.

#### User alerts
* All forms validate passed information before submission. If invalid information is inserted to the form, user is provided with actionable feedback.
* Users are informed about success/failure of their actions by means of contextual feedback messages.
* In case of 403, 404 and 500 http status errors, respective customized error page is displayed allowing user to navigate to safe website location. 


##### Home Page:

![Home Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/home-page.jpg "Home Page")

##### Posts filtered by author:

![Posts by Author Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/posts-by-author.jpg "Posts by Author Page")

##### Post:

![Post Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/post-page.jpg "Post Page")

##### Register Page:

![Register Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/register-page.jpg "Register Page")

##### Login Page:

![Login Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/login-page.jpg "Login Page")

##### Password Reset Pages:

![Password Reset Request Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/password-reset-request.jpg "Password Reset Request Page")

![Password Reset Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/password-reset.jpg "Password Reset Page")

##### Account Page:

![Account Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/account-page.jpg "Account Page")

##### New Post Page:

![New Post Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/new-post.jpg "New Post Page")

##### Update/Delete Post Page:

![Update/Delete Post Page](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/update-delete-post.jpg "Update/Delete Post Page")

##### User Alerts (Examples):

![User Alert Example 1](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/alert-example1.jpg "User Alert Example 1")

![User Alert Example 2](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/alert-example2.jpg "User Alert Example 2")

![User Alert Example 3](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/alert-example3.jpg "User Alert Example 3")

![User Alert Example 4](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/alert-example4.jpg "User Alert Example 4")

##### Error Pages (Example)

![Error Page Example](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/error-page.jpg "Error Page Example")

### Strategy

The FlyHigh blogging application was designed while keeping both computer and mobile devices users in mind. 
In order to achieve a positive user experience principles for minimalistic and defensive web design were applied.

### Scope

Demonstration of CRUD (Create, Read, Update and Delete) functionalities at the level of blog posts while applying basic business logic (i.e. user managment). 

### Skeleton
[Website wireframe](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/Wireframe.pdf)

### Surface
Greyscale color scheme.

## Technologies

### Front-end
1. HTML
1. CSS
1. Bootstrap

### Back-end
1. MongoDB
1. Python
1. Flask
1. Flask Blueprint
1. Flask Pymongo
1. Flask WTF
1. Flask Mail
1. Flask Paginate
1. Jinja Templates
1. Pillow
1. Werkzeug Security
1. itsdangerous TimedJSONWebSignatureSerializer
1. BSON

## Database architecture

![Database Architecture](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/database_structure.jpg "Database Architecture")

## Features
* Interactive design
* Responsive design
* Flask Blueprint powered application modularity
* MongoDB powered back-end
* Comprehensive User managment
* User accounts CRU functions
* Blog posts CRUD functions
* Password reset via e-mail
* Storing pictures as binary data in MongoDB
* Custom error pages
* User alerts
* Functionalities for maintaining data consistency in database and optimizing database size (e.g. when updating profile image, the old image is deleted from the database before the new one is uploaded)
* Resizing pictures before upload to database to optimize performance

