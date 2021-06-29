from flask import Flask

app = Flask(__name__)

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    pass
# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    pass
# GET /store
@app.route('/store')
def get_store():
    pass
# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item():
    pass
# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item():
    pass


app.run(port=5000)