from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)

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

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()  # only adding to this function to make testing easier/quicker
    def get(self, name):
        """Return back item based on name

        Args:
            name (String): Name of item to search

        Returns:
            Dictionary: Item found
        """
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404  # 404 is for not found

    def post(self, name):
        """Creates an item

        Args:
            name (string): Name of item

        Returns:
            Dictionary: Newly created item.
        """
        # if the content-type is not set or the body of the request is not in JSON format, we will get a failure in line 16. To avoid these failures we can use the following 2 solutions.
        # force=True - this means that you do not need the "content-type" to be set, it will look in the content and format it even if the content-type is not set. This is not recommended as then you will never look at the header and ALWAYS perform the processing to format the body into JSON
        # silent=True - this does not give an error and returns None
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {
                "message": "An item with name '{}' already exists".format(name)
            }, 400  # 400 is for a bad request because the user should've already known that an item with that name already exists

        data = Item.parser.parse_args()

        item = {"name": name, "price": data["price"]}
        items.append(item)
        return (
            item,
            201,
        )  # 201 is used for "created", 202 is when you are delaying the creation because maybe it takes 10 mins to create your object. At that point the client gets a successful return code and can move along

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    def get(self):
        """Returns back a list of items

        Returns:
            Dictionary: List of items
        """
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1:5000/item/<>
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(debug=True)  # important to mention debug=True
