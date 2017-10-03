from pymongo import MongoClient


def get_db():
    try:
        client = MongoClient('mongodb://vinh:Lazymonkey3#@35.164.154.80/discord_data')
        db = client.discord_data
        messages = db.messages
        return client, db, messages
    except Exception as e:
        print(e)
        print('database failed')
        return None


def get_client():
    try:
        mongo_client = MongoClient('mongodb://vinh:Lazymonkey3#@35.164.154.80/discord_data')
        return mongo_client
    except Exception as e:
        print(e)
        return None


def get_collection(db):
    try:
        collection = db.messages
        return collection
    except Exception as e:
        print(e)
        return None