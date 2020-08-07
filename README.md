# FlyHigh Blog: Bloggig application for aviation professionals and enthusiasts
Code Institute - Third Milestone Project: Data Centric Development

The blogging application was developed for authors wanting to share their opinions and experience from the field of civil aviation, and for the readers craving for the latest aviation news.

## Demo
A live demo of the website has been developed [here](http://fly-high-blog.herokuapp.com/).

![Responsive Web Demo](https://github.com/milan-stefanik/FlyHigh/blob/master/readme/demo.gif "Responsive Web Demo")


Responsive Web Demo GIF image was recorded using [Am I Responsive?](http://ami.responsivedesign.is) website. 

## UX

### User stories

#### Non-registered user
* User can access home page with a list of published posts.
* User can read published posts.
* User can filter posts by author (either through links in navigation bar or by clicking on post's author name).
* User can register and thus become a registered user (either through a link in navigation bar or by means of Login page).
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

The FlyHigh blogging application was designed while keeping both computer and mobile device users in mind. 
In order to achieve a positive user experience principles for minimalistic and defensive web design were applied.

### Scope

Demonstration of CRUD (Create, Read, Update and Delete) functionalities at the level of blog posts while applying basic business logic (i.e. user managment).
At user level, only CRU functionalities are available. 

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
1. Flask Session
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
* Comprehensive User management
* User accounts CRU functions
* Blog posts CRUD functions
* Password reset via e-mail
* Storing pictures as binary data in MongoDB
* Custom error pages
* User alerts
* Functionalities for maintaining data consistency in database and optimizing database size (e.g. when updating profile image, the old image is deleted from the database before the new one is uploaded; when deleting posts, all linked data is deleted as well)
* Resizing pictures before upload to database to optimize performance

## Testing

### Code validity
* HTML was tested via W3C Markup Validation Service
* CSS was tested via W3C CSS Validation Service
* Python code was thoroughly reviewed when implemeting application modularity using Flask Blueprint

#### Discovered bugs and drawbacks
* W3C Using Markup Validation Service is not practical for testing Jinja templates. 

### User stories
* During development process, each implemented functionality was tested individually
* Overall application function was tested manually following the particular user stories

#### Discovered bugs and drawbacks
* During testing in the GitPod, sending password reset e-mails did not work. After investigation, it was discovered that GitPod is blocking this function. Deployed version worked correctly.
* There was a problem with displaying author's name in the posts. The problem was solved by converting MongoDB object to list of dictionaries.
* Flask-Login powered user manamement did not work properly with PyMongo. The problem was solved by implementation of Flask Session based user managment instead of using Flask-Login.

### Data consistency in database
* Data stored in database were checked manually after every change through application user interface to assure data quality and consistency.

#### Discovered bugs and drawbacks
* As MongoDB is not a relational database, the issues with DELETE and UPDATE cascading had to be solved programatically.

### Browsers and devices
* Responsiveness has been tested using Inspect feature of Chrome and also on [Am I Responsive?](http://ami.responsivedesign.is) website.
* Website has been tested on iPhone XS plus using Chrome and Safari browsers. Other mobile devices screen sizes were emulated via Chrome Inspect feature.
* Website has been tested on multiple browsers in Windows (Chrome, Opera, Edge, Firefox and Internet Explorer) and multiple browsers in MacOs (Safari and Chrome).

#### Discovered bugs and drawbacks
* Post content is saved to MongoDB as string. To display post pararagraps as defined by the author, CSS property "white-space: break-spaces" is used. Then the text is justified using "text-align" and "text-align-last" properties. The text-alignment is correctly displayed in all browsers with exception of MacOs Safari and iOS Safari and Chrome. In these browsers, text is aligned to left.
* CSS property "text-overflow: ellipsis" did not work properly on iOS devices (this feature was intended to be used for displaying list of posts). Problem was solved by implementation of text fading effect.

## Deployment
The website is hosted on Heroku pages and can be accessed via this [link](http://fly-high-blog.herokuapp.com/). Heroku application is directly connected with the GitHub repository and automatic deploys are enabled. All changes are automatically reflected in production after each push to GitHub.

In order to make sure the deployed application works correctly:
* Config Variables in Heroku app needs to be properly set and kept up-to-date
* Correct Procfile needs to be in GitHub repository refering to app.py
* Requirements.txt file needs to be kept up-to-date listing all the required python packages
* Debug mode in app.py needs to be switched off (i.e. debug=False) in app.py
* env.py containg required secrets needs to be included in .gitignore file so as the secrets are not exposed

To run locally, repository can be cloned directly into the chosen editor by pasting `git clone https://github.com/milan-stefanik/FlyHigh.git` into terminal. To cut ties with this GitHub repository, `git remote rm origin` shall be used. Python3 and all python packages listed in requirements.txt need to be installed. It is recommended to install required python packages and run the application in virtual environment. Environment variables need to be set before running the application.

## Futher Development
Thanks to Flask Blueprint, FlyHigh blog application is easily scalable and modular. This allow adding other functionalities in the future.

Following functionalities could be added in the future:
* Post comment section allowing readers to leave a comment under each post.
* Full text search.
* Implementation of post tags and post categories.

## Credits

### Content
The listed posts are only for demonstration purposes and were copied from following sources:
* Air NZ swaps landing slots with United Airlines at Heathrow in secret deal [www.stuff.co.nz](https://www.stuff.co.nz/business/industries/122286760/air-nz-swaps-landing-slots-with-united-airlines-at-heathrow-in-secret-deal)
* Airbus trims A350 output, quarterly loss worse than expected [www.reuters.com](https://www.reuters.com/article/us-airbus-results/airbus-trims-a350-output-amid-larger-than-expected-second-quarter-loss-idUSKCN24V0II)
* JetBlue CEO warns of ‘day of reckoning’ for airlines as coronavirus continues to devastate demand [www.cnbc.com](https://www.cnbc.com/2020/07/29/jetblue-ceo-robin-hayes-government-aid-for-airlines-will-save-jobs.html?&qsearchterm=airlines)
* Boeing CEO ‘hopeful’ aircraft demand starts to recover in second half of 2021 [www.cnbc.com](https://www.cnbc.com/2020/07/29/boeing-ceo-hopeful-aircraft-demand-starts-to-recover-in-second-half-of-2021.html?&qsearchterm=airlines)
* Air cargo recovery continues to creep forward in June [asiacargobuzz.com](https://asiacargobuzz.com/2020/07/29/air-cargo-recovery-continues-to-creep-forward-in-june/)
* British Airways offers £1 flights to Europe under loyalty scheme as airlines fight decline in demand [uk.news.yahoo.com](https://uk.news.yahoo.com/british-airways-offers-1-flights-212111528.html)
* Rise in domestic travel helps smaller airlines [www.koreaherald.com](http://www.koreaherald.com/view.php?ud=20200728000676)
* Copa Airlines aims to restart operations in early September [www.reuters.com](https://www.reuters.com/article/us-copa-holdings-panama/copa-airlines-aims-to-restart-operations-in-early-september-idUSKCN24T07J)
* Portugal's TAP aims to resume 40 pct of flights in September [www.xinhuanet.com](http://www.xinhuanet.com/english/2020-07/27/c_139244244.htm)
* Passengers of Air France flights to Bengaluru to undergo COVID-19 test [in.news.yahoo.com](https://in.news.yahoo.com/passengers-air-france-flights-bengaluru-undergo-covid-19-090412703.html)
* Airline slot waivers need strict conditions: ACI World chief [www.flightglobal.com](https://www.flightglobal.com/networks/airline-slot-waivers-need-strict-conditions-aci-world-chief/139480.article)
* Delta Targets Virus Tests for All Employees in Next Four Weeks [www.bloomberg.com](https://www.bloomberg.com/news/articles/2020-07-23/delta-targets-virus-tests-for-all-employees-in-next-four-weeks)
* Emirates covers customers from COVID-19 expenses, in industry-leading initiative to boost travel confidence [www.emirates.com](https://www.emirates.com/media-centre/emirates-covers-customers-from-covid-19-expenses-in-industry-leading-initiative-to-boost-travel-confidence/)
* Southwest posts $915 million loss, warns travel demand will remain weak without coronavirus vaccine [www.cnbc.com/](https://www.cnbc.com/2020/07/23/southwest-airlines-luv-posts-second-quarter-loss.html)
* American Airlines posts $2.1 billion net loss in second quarter [www.cnbc.com](https://www.cnbc.com/2020/07/23/american-airlines-aal-posts-2point1-billion-loss-in-second-quarter-warns-on-coronavirus.html)
* Emirates offers pilots, cabin crew four months unpaid leave [www.reuters.com](https://www.reuters.com/article/us-health-coronavirus-emirates-airline/emirates-offers-pilots-cabin-crew-four-months-unpaid-leave-idUSKCN24O1D4?il=0)
* Uncertain future for airlines amid COVID-19 crisis [www.ktvu.com](https://www.ktvu.com/news/uncertain-future-for-airlines-amid-covid-19-crisis)
* United CEO: We won't be 'anywhere close to normal' until there's vaccine [edition.cnn.com](https://edition.cnn.com/2020/07/21/investing/united-airlines-earnings-covid/index.html)

### Media
* Images were downloaded from [Shutterstock](https://www.shutterstock.com/), [Pexels](https://www.pexels.com/), [Unsplash](https://unsplash.com/) and other royalty free image libraries.
* All the icons used come from [Font Awesome](https://fontawesome.com/), an free icon library.
* Navbar hover effect was downloaded from [Hover.css](https://ianlunn.github.io/Hover/) library.

### Acknowledgements
Following online tutorials were used as references while developing this project:
* Python Flask Tutorial by Corey Schafer [youtube.com](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)
* Creating a User Login System Using Python, Flask and MongoDB by Pretty Printed [youtube.com](https://www.youtube.com/watch?v=vVx1737auSE)
* Save and Retrieve Files In a MongoDB With Flask-Pymongo by Pretty Printed [youtube.com](https://www.youtube.com/watch?v=DsgAuceHha4)

Other references used:
* The Ultimate Flask Course by Anthony Herbert (available on packtpub.com)
* Flask by Example by Gareth Dwyer (available on packtpub.com)
* Mastering Flask Web Development - Second Edition by Daniel Gaspar, Jack Stouffer (available on packtpub.com)
* [stackoverflow.com](https://stackoverflow.com/)
* Code Institute Slack
* Code Institute Tutor Support

### Test link
<a href="http://www.google.com" target="_blank">Launch Google in a new window</a>


**This website was developed for educational purposes only** 