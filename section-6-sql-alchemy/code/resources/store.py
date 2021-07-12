from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()  # only adding to this function to make testing easier/quicker
    def get(self, name):
        """Return back store based on name

        Args:
            name (String): Name of store to search

        Returns:
            Dictionary: Store found
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name):
        """Creates an store

        Args:
            name (string): Name of store

        Returns:
            Dictionary: Newly created store.
        """
        # check if store already exists
        if StoreModel.find_by_name(name):
            return {"message": f"A store with name {name} already exists"}, 404

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occured inserting the store."}, 500

        return store.json(), 201
        # 201 is used for "created", 202 is when you are delaying the creation because maybe it takes 10 mins to create your object. At that point the client gets a successful return code and can move along

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted"}, 200


class StoreList(Resource):
    def get(self):
        """Returns back a list of items

        Returns:
            Dictionary: List of items
        """
        # query.all() returns all objects in table
        # list comprehension to get json of each store
        # return {"items": list(map(lambda x: x.json(), StoreModel.query.all()))}
        return {"stores": [store.json() for store in StoreModel.query.all()]}
