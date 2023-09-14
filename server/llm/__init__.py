import sys, os
from config import config
rel_path = os.path.join(os.path.dirname(__file__), ".")
abs_path = os.path.abspath(rel_path)
sys.path.insert(1, abs_path)

from openaillm import llm
from dallellm import *
if config.UseGpuImageGen:
    from kandinskyllm import *
    from stablediffusionllm import *