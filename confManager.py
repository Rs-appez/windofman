from pathlib import Path
import json
from tools import get_character_name

class ConfManager():

    @staticmethod
    def get_initiative(windows, ewmh) -> dict():
        conf_file = Path("config.json")
        if not conf_file.is_file() :
            with open("config.json",'w') as cf :
                cf.write('{}')
            conf_file = Path("config.json")

        initiative = json.load(conf_file.open())

        for window in windows:
            if not get_character_name(ewmh.getWmName(window)) in initiative:
                initiative[get_character_name(ewmh.getWmName(window))] = 0

        with open("config.json",'w') as cf :
            json.dump(initiative, cf)

        return initiative
    
    