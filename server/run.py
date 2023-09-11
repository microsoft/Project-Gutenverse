import os
from app import app


# Set the path to the stories directory
stories_directory = "/stories"

# Create the stories directory if it doesn't exist
if not os.path.exists(stories_directory):
    os.makedirs(stories_directory)

# DB configurations can happen here ect

if __name__ == "__main__":
    app.run(debug=True)