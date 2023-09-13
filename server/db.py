from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import WriteError, OperationFailure, ServerSelectionTimeoutError
from utilities import story_title_to_hash
class DB:
    # Static DB connection
    connection = None

    @staticmethod
    def connect(mongo_connection_string):
        try:
            client = MongoClient(mongo_connection_string)
            DB.connection = client["Project-GutenVerse"]
        except OperationFailure as e:
            print(f"Unable to connect to MongoDB: {e}")
        except ServerSelectionTimeoutError as e:
            print(f"MongoDB connection timed out: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def add_story_to_psuedo_index(title, id_=None):
        if not id_:
            id_ = story_title_to_hash(title)
        try:
            created_date = datetime.now()
            story = {
                "Title": title,
                "Id": id_,
                "_id": id_,
                "CreatedDate": created_date
            }
            new_story_id = DB.connection["Stories"].update_one({"_id": id_}, {'$set': story}, upsert=True)
        except WriteError as e:
            print(f"Insertion into MongoDB failed: {e}")
        except ServerSelectionTimeoutError as e:
            print(f"MongoDB connection timed out: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return story

    @staticmethod
    def delete_bad_stories():
        bad_stories = [x for x in DB.get_all_stories() if type(x['_id']) is ObjectId ]
        for bad_story in bad_stories:
            DB.connection["Stories"].delete_one({"_id": bad_story["_id"]})
        

    @staticmethod
    def get_all_stories():
        stories = None
        try:
            stories = DB.connection["Stories"].find()
        except OperationFailure as e:
            print(f"Getting all stories from MongoDB failed: {e}")
        except ServerSelectionTimeoutError as e:
            print(f"MongoDB connection timed out: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return stories
