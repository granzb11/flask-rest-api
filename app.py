import os

# third-party imports
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

# local imports
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# This turns off the FLASK SQLAlchemy modification tracker
# This does NOT turn off the SQLAlchemy modification tracker
# In order to know when an object had changed but not been saved to the database
# the extension flask SQLAlchemy was tracking every change that we made to the SQLAlchemy session and took some resources
# Now we're turning it off because SQLAlchemy itself, the main library, has it's own miodification tracker
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL_V2', 'sqlite:///data.db')
# this key should be secured somewhere, not within our code, don't check into version control
app.secret_key = "gustavo"
api = Api(app)



jwt = JWT(app, authenticate, identity)  # creates new endpoint /auth

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1:5000/item/<>
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
