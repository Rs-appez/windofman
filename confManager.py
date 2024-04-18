from pathlib import Path
import json
from tools import get_character_name

CONF_FILE = f"{Path( __file__ ).parent.absolute()}/config.json"

default_conf = '{"Initiatives":{}}'

class ConfManager():

    @staticmethod
    def get_json() -> json:
        content = None
        try :
            with open(CONF_FILE,'r') as cf:
                content = json.load(cf)
        except FileNotFoundError:
            with open(CONF_FILE,'x') as cf :
                cf.write(default_conf)
        except Exception as e:
            print("Error",e)
        finally:    
            if not content:
                content = json.loads(default_conf)
        return content

    @staticmethod
    def get_initiative(windows, ewmh) -> dict:

        try :
            initiative = ConfManager.get_json()["Initiatives"]
        
        except KeyError:
            initiative = {}

        for window in windows:
            character_name = get_character_name(ewmh.getWmName(window))
            if (character_name not in initiative 
                or not isinstance(initiative[character_name]['initiative'], int)) : 
                    initiative[character_name] = { 'initiative': 0, "ignore" : False}
                      

        ConfManager.__save_initiative(initiative)

        return initiative


    @staticmethod
    def set_initiative(values):
        initiative = ConfManager.get_json()["Initiatives"]
        for key,value in values.items():

            if 'Dofus' in key:
                key = key[:9]

            if 'Ini_' == key[:4] :
                try :
                    value = int(value)
                except ValueError:
                    value = 0
                initiative[key[4:]]['initiative'] = value
            elif 'Ign_' == key[:4] :
                try :
                    value = bool(value)
                except ValueError:
                    value = False
                initiative[key[4:]]['ignore'] = value

        ConfManager.__save_initiative(initiative)

    @staticmethod
    def __save_initiative(initiative):
        config = ConfManager.get_json()
        config['Initiatives'] = initiative
        with open(CONF_FILE,'w') as cf :
            json.dump(config, cf)
