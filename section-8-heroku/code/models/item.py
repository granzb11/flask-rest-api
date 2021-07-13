from db import db

# we are extending the Model class here and what that's going to do is tell SQLAlchemy that this class here
# are things that we are going to be saving to a database and retrieving from a database
# It's going to create that mapping between the database and the object/class
class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # setting up relationship  between ItemModel and StoreModel,
    # normally we would have to perform a join to get back an item tied to a specific store
    # with sql alchemy, setting up that relationship will create that link and thus we won't
    # need to do any crazy joins
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        # sqlalchemy handles all of the connection and cursor creation for us
        # SELECT * FROM items WHERE name=name LIMIT 1
        # this ends up returning an ItemModel object
        return cls.query.filter_by(name=name).first()
