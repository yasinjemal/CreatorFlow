from flask import g, current_app
from pymongo import MongoClient

def get_db():
    if 'db' not in g:
        uri = current_app.config['MONGODB_URI']
        g.db_client = MongoClient(uri)
        g.db = g.db_client.get_default_database()
        g.db.users.create_index("email", unique=True)
        g.db.oauth_tokens.create_index([("user_id",1),("platform",1)], unique=True)
    return g.db

def close_db(e=None):
    client = g.pop('db_client', None)
    if client is not None:
        client.close()
