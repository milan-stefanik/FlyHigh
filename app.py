# Importing os to have access to sytem-based functions and variables
import os
# Importing create_app function
from flyhighblog import create_app

app = create_app()

# When running app.py module as main program Python assigns
#   hard-coded string "__main__" to the __name__ variable
# If this is the case the application is run with below
#   defined parameters
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
