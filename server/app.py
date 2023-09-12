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