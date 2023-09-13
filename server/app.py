import os
import json
from flask import Flask, request, jsonify, send_from_directory
from mimetypes import guess_type
from config import config
from pipeline import Pipeline
from pipeline import PipelineContext
from db import DB

app = Flask(__name__)

@app.route("/stories/<story_id>/<chapter_number>/assets/<filename>", methods=["GET"])
def serve_chapter_asset(story_id, chapter_number, filename):
    chapter_path = os.path.join(config.server_root, config.stories_dir, story_id, chapter_number)
    
    if not os.path.exists(chapter_path):
        return jsonify({"error": "Chapter not found."}), 404

    return send_from_directory(chapter_path, filename, as_attachment=True, mimetype=guess_type(filename)[0])


@app.route("/stories/<story_id>/scene", methods=["GET"])
def get_scenes_from_disk(story_id):
    story_path = os.path.join(config.server_root, config.stories_dir, story_id)
    if not os.path.exists(story_path):
        return jsonify({"error": "Story not found."}), 404
    
    chapters = []
    chapter_dirs = sorted([d for d in os.listdir(story_path) if os.path.isdir(os.path.join(story_path, d)) and d.isdigit()], key=int)
    
    for chapter_dir in chapter_dirs:
        scene_file_path = os.path.join(story_path, chapter_dir, "scene.json")
        if os.path.exists(scene_file_path):
            with open(scene_file_path, "r") as file:
                data = json.load(file)
                chapters.append({
                    "Title": data.get("title", ""),
                    "Chapter": chapter_dir
                })
    
    return jsonify(chapters)                                   

@app.route("/stories/<story_id>/chapters_index", methods=["GET"])
def get_chapters_from_disk(story_id):
    story_path = os.path.join(config.server_root, config.stories_dir, story_id)
    if not os.path.exists(story_path):
        return jsonify({"error": "Story not found."}), 404
    
    chapters = []
    chapter_dirs = sorted([d for d in os.listdir(story_path) if os.path.isdir(os.path.join(story_path, d)) and d.isdigit()], key=int)
    
    for chapter_dir in chapter_dirs:
        scene_file_path = os.path.join(story_path, chapter_dir, "scene.json")
        if os.path.exists(scene_file_path):
            with open(scene_file_path, "r") as file:
                data = json.load(file)
                chapters.append({
                    "Title": data.get("title", ""),
                    "Chapter": chapter_dir
                })
    
    return jsonify(chapters)

@app.route("/chargen", methods=["GET"])
def chargen_test():
    context = PipelineContext(title="Chargen Test", story_data="If you wrote this to disk you failed.")    
    pipeline = Pipeline()
    pipeline.execute(context)
    return jsonify("It worked, amazing!!!!")


@app.route("/stories/disk", methods=["GET"])
def get_stories_from_disk():
    stories_dir = os.path.join(config.server_root, config.stories_dir)
    if not os.path.exists(stories_dir):
        return jsonify([])
    subfolders = [os.path.join(stories_dir, d) for d in os.listdir(stories_dir) if os.path.isdir(os.path.join(stories_dir, d))]
    if not subfolders:
        return jsonify([])
    stories_collection = []
    for folder in subfolders:
        stories_file = os.path.join(folder, "story.json")
        if os.path.exists(stories_file):
            with open(stories_file, "r") as file:
                data = json.load(file)
                stories_collection.append({
                    "Id": data["id"],
                    "Title": data["title"]
                })
    return jsonify(stories_collection)

@app.route("/stories", methods=["GET"])
def get_stories():
    mock_data = [
        {"Id":"d34c515d-4eb2-4a76-b878-da6d2a4d45c6", "Title": "The Tortoise and the Hare", "Summary": "Overconfidence leads the fast hare to lose a race to the steady tortoise."},
        {"Id":"926dcbde-3f37-4284-89a6-f0953a2292be","Title": "The Lion and the Mouse", "Summary": "A small mouse saves a lion, proving that even the weak can help the strong."},
        {"Id":"d4a3f22d-5c91-40c9-803d-9b58cb80ddd9","Title": "The Wolf And The Lamb", "Summary": "A wolf uses false accusations to justify eating an innocent lamb."}
    ]
    
    return jsonify(mock_data)

@app.route("/stories", methods=["POST"])
def create_story():
    data = request.get_json()
    if not data or 'title' not in data or not data['title'] or 'body' not in data or not data['body']:
        return {"error": "Invalid payload. 'title' and 'body' fields are required and should be non-empty."}, 400

    context = process_story(data['title'], data['body'])
    return {"guid": context.id}, 201

@app.route("/upload_story", methods=["POST"])
def upload_story():
    title = request.form.get('title')
    uploaded_file = request.files.get('file')
    if not title:
        return {"error": "The 'title' field is required."}, 400
    if not uploaded_file:
        return {"error": "A file must be uploaded."}, 400

    story_data = uploaded_file.read().decode('utf-8')
    context = process_story(title, story_data)
    return {"guid": context.id}, 201

def process_story(title, story_data):
    context = PipelineContext(title=title, story_data=story_data)    
    pipeline = Pipeline()
    pipeline.execute(context)
    return context

# Create the stories directory if it doesn't exist
if not os.path.exists(config.stories_dir):
    os.makedirs(config.stories_dir)
    
# Provide the mongodb atlas url to connect python to mongodb using pymongo
# Create a connection using MongoClient
DB.connect(config.MongoDBConnectionString)

if __name__ == "__main__":
    app.run(debug=True)
