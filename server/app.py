import os
import json
import uuid
from flask import Flask, request, jsonify
from config import config
from pipeline import Pipeline
from pipelinecontext import PipelineContext
app = Flask(__name__)

@app.route("/stories", methods=["GET"])
def get_stories():
    stories_directory = config.stories_dir
    # List subdirectories under the stories_directory
    story_dirs = [d for d in os.listdir(stories_directory) if os.path.isdir(os.path.join(stories_directory, d))]
    return jsonify(story_dirs)

@app.route("/stories", methods=["POST"])
def create_story():
    data = request.get_json()
    if not data or 'title' not in data or not data['title'] or 'body' not in data or not data['body']:
        return jsonify({"error": "Invalid payload. 'title' and 'body' fields are required and should be non-empty."}), 400

    context = process_story(data['title'], data['body'])
    return jsonify({"guid": context.id}), 201

@app.route("/upload_story", methods=["POST"])
def upload_story():
    title = request.form.get('title')
    uploaded_file = request.files.get('file')
    if not title:
        return jsonify({"error": "The 'title' field is required."}), 400
    if not uploaded_file:
        return jsonify({"error": "A file must be uploaded."}), 400

    story_data = uploaded_file.read().decode('utf-8')
    context = process_story(title, story_data)
    return jsonify({"guid": context.id}), 201

def process_story(title, story_data):
    context = PipelineContext()
    context.title = title
    context.story_data = story_data
    
    pipeline = Pipeline()
    pipeline.execute(context)
    return context