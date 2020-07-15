# Importing os to have access to sytem-based functions and variables
import os
# Importing app variable from flyhighblog folder from __init__.py
from flyhighblog import app

# When running app.py module as main program Python assigns
#   hard-coded string "__main__" to the __name__ variable
# If this is the case the application is run with defined parameters
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
