import os
import yaml

CONFIG_FILE = os.path.expanduser("~/.devdash.yaml")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return yaml.safe_load(file)
    else:
        return {}

def save_config(data):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(data, file)

def set_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)

def get_config(key):
    config = load_config()
    return config.get(key)
