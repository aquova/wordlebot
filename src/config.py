import json

DATABASE_PATH = "/private/wordle.db"
_CONFIG_PATH = "/private/config.json"
with open(_CONFIG_PATH) as config_file:
    cfg = json.load(config_file)

DISCORD_KEY = cfg['discord']
