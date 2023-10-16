from flask_app import app

#import controllers for application
from flask_app.controllers import users, magazines



if __name__ == '__main__':
    app.run(debug=True)