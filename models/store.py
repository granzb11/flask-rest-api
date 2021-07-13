# third-party imports
from db import db

# we are extending the Model class here and what that's going to do is tell SQLAlchemy that this class here
# are things that we are going to be saving to a database and retrieving from a database
# It's going to create that mapping between the database and the object/class
class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # self.items is no longer a list of items but instead becomes a query builder
    # TODO (Gustavo) need to do some more reading around this, short explanation during video 102
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self):
        return {"id": self.id, "name": self.name, "items": [item.json() for item in self.items.all()]}

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
