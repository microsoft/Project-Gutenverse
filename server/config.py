import yaml
import os
from dataclasses import dataclass
from pathlib import Path
# Secret management will be done through environment variables for now
# All non secret config items will be put in a config yaml file

# Ensure that paths are relative to the script's directory
_BASE_DIR = Path(__file__).parent
_CONFIG_FILE = Path('server/config.yaml')
_Secret_Identifier = 'EnvironmentVariables'

@dataclass
class Config:
    server_root: Path
    stories_dir: Path
    OpenAIApiKey: str
    MongoDBConnectionString: str
    
def get_secret(name):
    return os.getenv(name)

def _load_config():
    print(os.getcwd())
    
    with open(_CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
        config_with_secrets = {k: v if v != _Secret_Identifier else get_secret(k) for k, v in config.items()}
    
    config_with_secrets['server_root'] = _BASE_DIR
    return config_with_secrets

config = Config(**_load_config())

# New function to resolve paths based on serverRoot
def resolve_path(relative_path: str) -> Path:
    return config.server_root / relative_path
