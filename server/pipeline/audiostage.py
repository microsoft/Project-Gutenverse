from stage import Stage
from config import config
from audiocraft.models import AudioGen, MusicGen
from audiocraft.data.audio import audio_write
import json
import os
from loguru import logger
import time

class AudioStage(Stage):

    def __repr__(self) -> str:
        return 'AudioStage'

    def __str__(self) -> str:
        return self.__repr__()

    def __init__(self, _music_duration=5, _audio_duration=2):
        start = time.time()
        # Load the Music Gen model with the CPU if we are not using the GPU, otherwise let Music Gen determine how to load the model
        self.musicgen_model = MusicGen.get_pretrained('facebook/musicgen-small', device="cpu")
        end = time.time()
        logger.info(f"MusicGen Model took {end-start} seconds")

        self.musicgen_model.set_generation_params(duration=_music_duration)

        start = time.time()
        # Load the Audio Gen model with the CPU if we are not using the GPU, otherwise let Audio Gen determine how to load the model
        self.audiogen_model = AudioGen.get_pretrained('facebook/audiogen-medium', device="cpu")
        end = time.time()
        logger.info(f"AudioGen Model took {end-start} seconds")

        self.audiogen_model.set_generation_params(duration=_audio_duration)

    def _process(self, context):
        story_folder = os.path.join(config.server_root, config.stories_dir, context.id)
        music_filename = "music"
        audio_filename = "audio"

        for subfolder in sorted(os.listdir(story_folder)):
            subfolder_path = os.path.join(story_folder, subfolder)

            save_file_path = os.path.join(subfolder_path, '4_audio_stage.json')
            if os.path.isfile(save_file_path):
                logger.info(f"{self} step found to be already completed")

            # Check if the path is a directory and contains the required JSON file
            if os.path.isdir(subfolder_path) and '1_analysis_stage.json' in os.listdir(subfolder_path):
                json_path = os.path.join(subfolder_path, '1_analysis_stage.json')

                # Read the JSON file
                with open(json_path, 'r') as file:
                    data = json.load(file)
                    audio_data = data.get('audio', {})
                    mood_music = audio_data.get('mood', {})
                    sequence = audio_data.get('sequence', {})        
                    sound_effects = list(sequence.values())

                    self.generate_music(mood_music, subfolder_path, music_filename)
                    self.generate_audio(sound_effects, subfolder_path, audio_filename)

                    json_data = {
                        "audio":
                        {
                            "mood": mood_music,
                            "sequence": sequence,
                            "music_file": f"{music_filename}.wav",
                            "audio_files": {}
                        }
                    }

                    for idx in range(len(sound_effects)):
                        json_data["audio"]["audio_files"][idx+1] = f"{audio_filename}_sequence_{idx+1}.wav"

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

    def generate_audio(self, audio_prompt, path, filename):
        logger.info("AudioGen model about to generate...")
        start = time.time()
        wav = self.audiogen_model.generate(audio_prompt)  # generates samples.
        end = time.time()
        logger.info(f"AudioGen Generation took {end-start} seconds")

        for idx, one_wav in enumerate(wav):
            filepath = os.path.join(path, f"{filename}_sequence_{idx+1}")
            audio_write(filepath, one_wav.cpu(), self.audiogen_model.sample_rate, strategy="loudness", loudness_compressor=True)

