# third-party imports
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

# local imports
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
# This turns off the FLASK SQLAlchemy modification tracker
# This does NOT turn off the SQLAlchemy modification tracker
# In order to know when an object had changed but not been saved to the database
# the extension flask SQLAlchemy was tracking every change that we made to the SQLAlchemy session and took some resources
# Now we're turning it off because SQLAlchemy itself, the main library, has it's own miodification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# this key should be secured somewhere, not within our code, don't check into version control
app.secret_key = "gustavo"
api = Api(app)

# so JWT creates an /auth endpoint, this endpoint takes in username and password
# JWT will take that username and password and pass it to our authenticate() method in security.py
# our authetnicate method will return the user and with that user JWT will create a JW token and the endpoint will return that
# This is the auth token that our users will use within their headers to authenticate with us
# So the next API call the user performs, will use that token. JWT will then grab that and call identity() from security.py
# with that we will authenticate our users going forward
jwt = JWT(app, authenticate, identity)  # creates new endpoint /auth

api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1:5000/item/<>
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
