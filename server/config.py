import yaml
import os
from dataclasses import dataclass
from pathlib import Path
# Secret management will be done through enviroment variables for now
# All non secret config items will be put in a config yaml file

_CONFIG_FILE = Path('server/config.yaml')
_Secret_Identifier = 'EnviromentVariables'

@dataclass
class Config:
    stories_dir: Path
    OpenAIApiKey: str
    
def get_secret(name):
    return os.getenv(name)

def _load_config():
    print(os.getcwd())
    with open(_CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
        config_with_secrets = {k: v if v is not _Secret_Identifier else get_secret(k) for k, v in config.items()}
    return config_with_secrets


config = Config(**_load_config())