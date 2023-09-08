import os
import json
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set the path to the stories directory
stories_directory = "/stories"

# Create the stories directory if it doesn't exist
if not os.path.exists(stories_directory):
    os.makedirs(stories_directory)

@app.route("/stories", methods=["GET"])
def get_stories():
    # List subdirectories under the stories_directory
    story_dirs = [d for d in os.listdir(stories_directory) if os.path.isdir(os.path.join(stories_directory, d))]
    return jsonify(story_dirs)

@app.route("/stories", methods=["POST"])
def create_story():
    # Generate a new GUID
    new_guid = str(uuid.uuid4())

    # Create a new directory for the story
    new_story_directory = os.path.join(stories_directory, new_guid)
    os.makedirs(new_story_directory)

    # Save the story as a JSON file in the new directory
    story = request.json
    with open(os.path.join(new_story_directory, "story.json"), "w") as f:
        json.dump(story, f)

    return jsonify({"guid": new_guid}), 201

if __name__ == "__main__":
    app.run(debug=True)
