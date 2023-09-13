from audiocraft.models import AudioGen, MusicGen
from audiocraft.data.audio import audio_write
import time
import torch

try:
    torch.cuda.empty_cache()

    start = time.time()
    musicgen_model = MusicGen.get_pretrained('facebook/musicgen-small')
    end = time.time()
    print(f"MusicGen Model took {end-start} seconds")

    musicgen_model.set_generation_params(duration=5)  # generate 5 seconds.

    start = time.time()
    audiogen_model = AudioGen.get_pretrained('facebook/audiogen-medium')
    end = time.time()
    print(f"MusicGen Model took {end-start} seconds")

    audiogen_model.set_generation_params(duration=5) # generate 5 seconds

    while True:
        title = ""
        prompt = ""

        print("1: AudioGen")
        print("2: MusicGen")
        inp = input("Enter your choice:")
        if inp != "1" and inp != "2":
            continue

        print("Enter a title for the audio file")
        while title == "":
            title = input("Title:")

        print("Enter your prompt")
        while prompt == "":
            prompt = input("Prompt:")

        wav = None
        sample_rate = 0
        if inp == "1":
            print("AudioGen model about to generate...")
            start = time.time()
            wav = audiogen_model.generate([prompt])  # generates samples.
            end = time.time()
            print(f"AudioGen Generation took {end-start} seconds")
            sample_rate = audiogen_model.sample_rate
        elif inp == "2":
            print("MusicGen model about to generate...")
            start = time.time()
            wav = musicgen_model.generate([prompt])  # generates samples.
            end = time.time()
            print(f"MusicGen Generation took {end-start} seconds")
            sample_rate = musicgen_model.sample_rate

        audio_write(title, wav[0].cpu(), sample_rate, strategy="loudness", loudness_compressor=True)

except KeyboardInterrupt:
    print("Keyboard Interrupt exception caught")
    exit(0)
except Exception as e:
    print(f"Exception: {e}")