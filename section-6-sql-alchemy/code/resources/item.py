import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    TABLE_NAME = "items"
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
        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return item.json(), 201
         # 201 is used for "created", 202 is when you are delaying the creation because maybe it takes 10 mins to create your object. At that point the client gets a successful return code and can move along

    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        # example of "named style" for query formation vs question mark style
        if item is None: # item does not exist in database
            item = ItemModel(name, data['price'])
        else: # item does exist in database
            item.price = data['price']

        item.save_to_db()
        return {"item": updated_item.json()}


class ItemList(Resource):
    @classmethod
    def convert_tuples_to_dict(cls, keys: tuple, list_of_tuples: list) -> dict:
        """Converts list of tuples to dictionary
        # https://www.geeksforgeeks.org/python-convert-list-tuples-dictionary/

        Args:
            tuples_list (list): list of tuples

        Returns:
            dict: dictionary of conversion
        """
        tuples_dict = {}
        for tuple in list_of_tuples:
            # keys - (name, price)
            # tuple - (chair, 11.99)
            # temp_dict - {"name": "chair", "price": "11.99"}
            temp_dict = dict(zip(keys, tuple))

    def get(self):
        """Returns back a list of items

        Returns:
            Dictionary: List of items
        """
        items = []
        connection = sqlite3.connect("data.db")
        # this is to get the column names with results
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        rows = result.fetchall()

        # close connection
        connection.close()

        # convert sqlite row object to dicitonaries
        # add dictionary to list of dicitonaries
        for row in rows:
            items.append(dict(row))

        return {"items": items}, 200
