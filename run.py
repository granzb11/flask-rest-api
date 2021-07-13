from db import db
from app import app

db_init_app(app)

@app.before_first_request
# this will run before any request is served and it's going to create the tables for us if they don't already exist
def crate_tables():
    db.create_all()