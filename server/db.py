from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import WriteError, OperationFailure, ServerSelectionTimeoutError

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
    def create_story(title, path):
        story = None
        try:
            created_date = datetime.now()
            story = {
                "Title": title,
                "Path": path,
                "CreatedDate": created_date
            }
            new_story_id = DB.connection["Stories"].insert_one(story)
            story["_id"] = new_story_id.inserted_id
        except WriteError as e:
            print(f"Insertion into MongoDB failed: {e}")
        except ServerSelectionTimeoutError as e:
            print(f"MongoDB connection timed out: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return story

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
