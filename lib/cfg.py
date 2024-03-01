import json, os
from lib import log_init
log_init.logging.info("Basic libs imported at cfg.py")

cfgData = None
defaultJSON = """{
    "language": "sys",
    "appearances": [
        {
            "mode": "sys",
            "schemes": "blue",
            "rtl": false
        }
    ],
    "play": [
        {
            "immediatelyPlay": false,
            "defaultPlayInLoop": false,
            "defaultVolume": 100
        }
    ],
    "lyrics": [
        {
            "lyricsDefaultVisible": true
        }
    ],
    "online": [
        {
            "onlineAPI": "https://music.dsb.ink/api/"
        }
    ]
}
"""

def loadConfig():
    global cfgData, defaultJSON
    if not os.path.exists('config.json'):
        log_init.logging.info("No config.json found, creating a new one")
        f = open('config.json', 'w')
        f.write(defaultJSON)
        f.close()
        log_init.logging.info("config.json created")
    with open('config.json', 'r') as f:
        cfgData = json.load(f)
        f.close()
        log_init.logging.info("config.json loaded to cfgData")

def saveConfig():
    global cfgData
    with open('config.json', 'w') as f:
        json.dump(cfgData, f, indent = 4)
        f.close()
        log_init.logging.info("Config saved")