from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []
class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404 # 404 is for not found

    def post(self, name):
        item = {'name': name, 'price': 12.00}
        items.append(item)
        return item, 201 # 201 is used for "created", 202 is when you are delaying the creation because maybe it takes 10 mins to create your object. At that point the client gets a successful return code and can move along

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/<>
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)