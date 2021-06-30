from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []
class Item(Resource):
    def get(self, name):
        """Return back item based on name

        Args:
            name (String): Name of item to search

        Returns:
            Dictionary: Item found
        """
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404 # 404 is for not found

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
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists".format(name)}, 400 # 400 is for a bad request because the user should've already known that an item with that name already exists

        data = request.get_json(force=True)
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # 201 is used for "created", 202 is when you are delaying the creation because maybe it takes 10 mins to create your object. At that point the client gets a successful return code and can move along

class ItemList(Resource):
    def get(self):
        """Returns back a list of items

        Returns:
            Dictionary: List of items
        """
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/<>
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)