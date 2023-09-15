import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from mimetypes import guess_type
from config import config
from pipeline import Pipeline
from pipeline import PipelineContext
from db import DB
from loguru import logger
from bson import ObjectId
from collections import defaultdict

app = Flask(__name__)
CORS(app)

@app.before_request
def log_request_info():
    logger.info(f'{request.url_rule.rule=}\n{request.headers=}\n')

@app.route("/stories/<story_id>/<chapter_number>/assets/<filename>", methods=["GET"])
def serve_chapter_asset(story_id, chapter_number, filename):
    chapter_path = os.path.join(config.server_root, config.stories_dir, story_id, chapter_number)
    
    if not os.path.exists(chapter_path):
        return jsonify({"error": "Chapter not found."}), 404

    return send_from_directory(chapter_path, filename, as_attachment=True, mimetype=guess_type(filename)[0])


@app.route("/stories/<story_id>/scene", methods=["GET"])
def serve_story_scene(story_id):
    scene_path = os.path.join(config.server_root, config.stories_dir, story_id, "scene_compilation.json")
    
    if not os.path.exists(scene_path):
        return jsonify({"error": "Chapter not found."}), 404
    
    with open(scene_path, 'r') as file:
        data = json.load(file)

        return jsonify(data)

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
    return [x for x in DB.get_all_stories() if type(x['_id']) is not ObjectId ]
    
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
    DB.add_story_to_psuedo_index(title)
    context = PipelineContext(title=title, story_data=story_data)    
    pipeline = Pipeline()
    pipeline.execute(context)
    return context

@app.route("/AdminApi/ManualCrawl")
def manual_update_db():
    stories_dir = os.path.join(config.server_root, config.stories_dir)
    if not os.path.exists(stories_dir):
        logger.warning(f"There are no stories to manually insert. Look at {stories_dir}")
        return
    subfolders = [os.path.join(stories_dir, d) for d in os.listdir(stories_dir) if os.path.isdir(os.path.join(stories_dir, d))]
    if not subfolders:
        return []
    for folder in subfolders:
        stories_file = os.path.join(folder, "story.json")
        if os.path.exists(stories_file):
            with open(stories_file, "r") as file:
                data = json.load(file)
                DB.add_story_to_psuedo_index(data["title"], data["id"])
    return "Success"

@app.route("/AdminApi/RemoveBadDocuments")
def remove_bad_documents():
    DB.delete_bad_stories()
    return "Success"

@app.route("/AdminApi/PurgeDB")
def remove_documents():
    DB.delete_stories()
    return "Success"

@app.route("/stories/<story_id>/status")
def get_story_status(story_id):
    story_path = os.path.join(config.server_root, config.stories_dir, story_id)
    
    if not os.path.exists(story_path):
        return {"error": "Story Not found"}, 404
    
    stage_names = {
    'Analyizer': '1_analysis_stage.json',
    'CharacterGeneration': '2_charactergen_stage.json',
    'SkyboxGeneration': '3_skyboxgen_stage.json',
    'AudioGeneration': '4_audio_stage.json',
    'Composition': '4_composition_stage.json',
    'SceneCompilation': '5_scenecompilation_stage.json'
    }

    status = defaultdict(list)
    segmentation_done = False
    for potentail_scene_dir in os.listdir(story_path):
        potentail_scene_dir = os.path.join(story_path, potentail_scene_dir)
        if not os.path.isdir(potentail_scene_dir):
            continue
        segmentation_done = True
        for stage, file_name in stage_names.items():
            if not status.get(os.path.basename(potentail_scene_dir)):
                status[os.path.basename(potentail_scene_dir)] = []
            if os.path.isfile(os.path.join(potentail_scene_dir, file_name)):
               status[os.path.basename(potentail_scene_dir)].append(stage)
    if not segmentation_done:
        response = { "Number of Scenes": "Still being determined",
                 "Stages Left": list(stage_names.keys()) + ["Segmentation"],
                 "Current Scene and Stage": f'NA: Segementation',
                 }
        return response
    base_line = status['0']
    current_scene = '0'
    for scene, stages_done in status.items():
        if len(base_line) == len(stages_done):
            current_scene = scene
        elif len(base_line) > len(stages_done):
            current_scene = scene
            break
    current_stage = list(set(base_line) - set(stages_done))        
    response = { "Number of Scenes": len(status),
                 "Stages Left": [x for x in stage_names if x not in status['0']],
                 "Current Scene and Stage": f'{current_scene}: {current_stage}',
                 }
    return response

# Create the stories directory if it doesn't exist
if not os.path.exists(config.stories_dir):
    os.makedirs(config.stories_dir)
    
# Provide the mongodb atlas url to connect python to mongodb using pymongo
# Create a connection using MongoClient
DB.connect(config.MongoDBConnectionString)

if __name__ == "__main__":
    app.run(debug=True)
