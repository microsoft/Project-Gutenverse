from stage import Stage
from config import config
from audiocraft.models import AudioGen, MusicGen
from audiocraft.data.audio import audio_write
import json
import os
from loguru import logger
import time
from gtts import gTTS

class AudioStage(Stage):

    def __repr__(self) -> str:
        return 'AudioStage'

    def __str__(self) -> str:
        return self.__repr__()

    def __init__(self, _music_duration=5, _audio_duration=2):
        start = time.time()
        # Load the Music Gen model with the CPU if we are not using the GPU, otherwise let Music Gen determine how to load the model
        self.musicgen_model = MusicGen.get_pretrained('facebook/musicgen-small', device="cpu" if not config.UseGpuAudioGen else None)
        end = time.time()
        logger.info(f"MusicGen Model took {end-start} seconds")

        self.musicgen_model.set_generation_params(duration=_music_duration)

        start = time.time()
        # Load the Audio Gen model with the CPU if we are not using the GPU, otherwise let Audio Gen determine how to load the model
        self.audiogen_model = AudioGen.get_pretrained('facebook/audiogen-medium', device="cpu" if not config.UseGpuAudioGen else None)
        end = time.time()
        logger.info(f"AudioGen Model took {end-start} seconds")

        self.audiogen_model.set_generation_params(duration=_audio_duration)

    def _process(self, context):
        story_folder = os.path.join(config.server_root, config.stories_dir, context.id)
        music_filename = "music"
        audio_filename = "audio"
        tts_filename = "tts"

        for subfolder in sorted(os.listdir(story_folder)):
            subfolder_path = os.path.join(story_folder, subfolder)

            save_file_path = os.path.join(subfolder_path, '6_audio_stage.json')
            if os.path.isfile(save_file_path):
                logger.info(f"{self} step found to be already completed")
                continue

            # Check if the path is a directory and contains the required JSON files
            if os.path.isdir(subfolder_path):
                json_data = {}
                json_data["audio"] = {}

                if '1_analysis_stage.json' in os.listdir(subfolder_path):
                    json_path = os.path.join(subfolder_path, '1_analysis_stage.json')
                    # Read the JSON file
                    with open(json_path, 'r') as file:
                        data = json.load(file)
                        audio_data = data.get('audio', {})
                        mood_music = audio_data.get('mood', {})
                        sequence = audio_data.get('sequence', {})
                        story_sound_effects = list(sequence.values())

                        character_data = data.get('characters', {})
                        characters = list(character_data.keys())
                        character_sound_effects = []
                        for character in characters:
                            character_sound_effects.append(character_data[character]["soundeffect"])

                        self.generate_music(mood_music, subfolder_path, music_filename)
                        self.generate_story_audio(story_sound_effects, subfolder_path, audio_filename)
                        self.generate_characters_audio(character_sound_effects, subfolder_path, characters)
                        
                        json_data["audio"]["mood"] = mood_music
                        json_data["audio"]["sequence"] = sequence
                        json_data["audio"]["music_file"] = f"{music_filename}.wav"

                        json_data["audio"]["audio_files"] = {}
                        for idx in range(len(story_sound_effects)):
                            json_data["audio"]["audio_files"][idx+1] = f"{audio_filename}_sequence_{idx+1}.wav"

                        json_data["audio"]["character_sound_effects"] = {}
                        for character in characters:
                            json_data["audio"]["character_sound_effects"][character] = f"{character}.wav"

                if 'scene.json' in os.listdir(subfolder_path):
                    json_path = os.path.join(subfolder_path, 'scene.json')
                    # Read the JSON file
                    with open(json_path, 'r') as file:
                        data = json.load(file)
                        title = data.get('title', '')
                        storycontent = data.get('content', '')
                        storycontent = self.clean_white_space(storycontent)

                        self.generate_tts(f"{title}\n{storycontent}", subfolder_path, tts_filename)
                        json_data["audio"]["tts_file"] = f"{tts_filename}.mp3"
                
                if json_data:
                    with open(save_file_path, 'w') as output_file:
                        json.dump(json_data, output_file, indent=4)

        return context
    
    def generate_music(self, music_prompt, path, filename):
        logger.info("MusicGen model about to generate...")
        start = time.time()
        wav = self.musicgen_model.generate([music_prompt])  # generates samples.
        end = time.time()
        logger.info(f"MusicGen Generation took {end-start} seconds")

        filepath = os.path.join(path, filename)
        audio_write(filepath, wav[0].cpu(), self.musicgen_model.sample_rate, strategy="loudness", loudness_compressor=True)

    def generate_story_audio(self, story_audio_prompt, path, filename):
        logger.info("AudioGen model about to generate for story...")
        start = time.time()
        wav = self.audiogen_model.generate(story_audio_prompt)  # generates samples.
        end = time.time()
        logger.info(f"AudioGen Generation took {end-start} seconds")

        for idx, one_wav in enumerate(wav):
            filepath = os.path.join(path, f"{filename}_sequence_{idx+1}")
            audio_write(filepath, one_wav.cpu(), self.audiogen_model.sample_rate, strategy="loudness", loudness_compressor=True)

    def generate_characters_audio(self, characters_audio_prompt, path, filenames):
        logger.info("AudioGen model about to generate for characters...")
        print(characters_audio_prompt)
        print(filenames)
        start = time.time()
        wav = self.audiogen_model.generate(characters_audio_prompt)  # generates samples.
        end = time.time()
        logger.info(f"AudioGen Generation took {end-start} seconds")

        for idx, one_wav in enumerate(wav):
            filepath = os.path.join(path, f"{filenames[idx]}")
            audio_write(filepath, one_wav.cpu(), self.audiogen_model.sample_rate, strategy="loudness", loudness_compressor=True)

    def generate_tts(self, tts_prompt, path, filename):
        filepath = os.path.join(path, f"{filename}.mp3")
        logger.info("TTS about to generate...")

        start = time.time()
        tts = gTTS(tts_prompt, lang='en', tld='co.uk')
        tts.save(filepath)
        end = time.time()
        logger.info(f"TTS Generation took {end-start} seconds")
    
    def clean_white_space(self, str):
        return str.replace("\n", " ")
