from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    TABLE_NAME = "items"
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )
        parser.add_argument(
        "store_id", type=int, required=True, help="Every item needs a store id."
    )

    @jwt_required()  # only adding to this function to make testing easier/quicker
    def get(self, name):
        """Return back item based on name

        Args:
            name (String): Name of item to search

        Returns:
            Dictionary: Item found
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        """Creates an item

        Args:
            name (string): Name of item

        Returns:
            Dictionary: Newly created item.
        """
        # check if item already exists
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists"}, 404

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return item.json(), 201
         # 201 is used for "created", 202 is when you are delaying the creation because maybe it takes 10 mins to create your object. At that point the client gets a successful return code and can move along

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        # example of "named style" for query formation vs question mark style
        if item is None: # item does not exist in database
            item = ItemModel(name, **data)
            # item = ItemModel(name, data['price'], data['store_id'])
        else: # item does exist in database
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return {"item": item.json()}

class ItemList(Resource):
    def get(self):
        """Returns back a list of items

        Returns:
            Dictionary: List of items
        """
        # query.all() returns all objects in table
        # list comprehension to get json of each item
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {"items": [item.json() for item in ItemModel.query.all()]}
