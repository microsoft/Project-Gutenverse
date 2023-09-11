import os
import json
import uuid
from flask import Flask, request, jsonify
from config import config
app = Flask(__name__)

@app.route("/stories", methods=["GET"])
def get_stories():
    stories_directory = config.stories_dir
    # List subdirectories under the stories_directory
    story_dirs = [d for d in os.listdir(stories_directory) if os.path.isdir(os.path.join(stories_directory, d))]
    return jsonify(story_dirs)

@app.route("/stories", methods=["POST"])
def create_story():
    # Generate a new GUID
    new_guid = str(uuid.uuid4())
    # todo: refactor to run pipeline with the new story payload

    return jsonify({"guid": new_guid}), 201


