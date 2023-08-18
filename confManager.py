from pathlib import Path
import json
from tools import get_character_name

CONF_FILE = "config.json"

class ConfManager():

    @staticmethod
    def __check_conf_file():
        conf_file = Path(CONF_FILE)
        if not conf_file.is_file() :
            with open(CONF_FILE,'x') as cf :
                cf.write('{}')    
                
    @staticmethod
    def __get_json() -> json:
        try :
            with open(CONF_FILE,'r') as cf:
                content = json.load(cf)
        except json.JSONDecodeError :
            content = json.loads('{}')
        return content

    @staticmethod
    def get_initiative(windows, ewmh) -> dict():
        
        ConfManager.__check_conf_file()

        initiative = ConfManager.__get_json()
        
        for window in windows:
            if not get_character_name(ewmh.getWmName(window)) in initiative:
                initiative[get_character_name(ewmh.getWmName(window))] = 0

        ConfManager.save_initiative(initiative)

        return initiative


    @staticmethod
    def set_initiative(values):

        initiative = ConfManager.__get_json()
        for key,value in values.items():
            try :
                value = int(value)
            except ValueError:
                value = 0
            initiative[key] = value    

        ConfManager.save_initiative(initiative)

    @staticmethod
    def save_initiative(initiative):
         with open(CONF_FILE,'w') as cf :
            json.dump(initiative, cf)
