from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import scipy
import time
import os
import json

def get_mood():
    file_path = os.path.join(".\sample_stories", "1_analysis_stage.json")
    print(file_path)
    
    f = open(file_path)
    data = json.load(f)

    return data['audio']['mood']

try:
    music_mood = get_mood()
    music_prompt = "Create catchy background music that is loopable, 120 bpm. Make the music relaxing to listen to for long periods of time. " + music_mood
    print(music_prompt)

    # get the model
    start = time.time()
    model = MusicGen.get_pretrained('facebook/musicgen-small')
    end = time.time()
    print(f"Model took {end-start} seconds")

    model.set_generation_params(duration=8)  

    # generate music
    start = time.time()
    wav = model.generate([music_prompt])
    end = time.time()
    print(f"Generation took {end-start} seconds")

    audio_write("test_mood_8sec", wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    
except Exception as e:
    print(f"Exception: {e}")