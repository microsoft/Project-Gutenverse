import os
from app import app
from config import config

# Create the stories directory if it doesn't exist
if not os.path.exists(config.stories_dir):
    os.makedirs(config.stories_dir)

# DB configurations can happen here ect

if __name__ == "__main__":
    app.run(debug=True)