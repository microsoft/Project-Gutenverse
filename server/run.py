import os
from app import app
from config import config
from db import DB

# Create the stories directory if it doesn't exist
if not os.path.exists(config.stories_dir):
    os.makedirs(config.stories_dir)

# DB configurations can happen here ect

# Provide the mongodb atlas url to connect python to mongodb using pymongo
# Create a connection using MongoClient
DB.connect(config.MongoDBConnectionString)

if __name__ == "__main__":
    app.run(debug=True)