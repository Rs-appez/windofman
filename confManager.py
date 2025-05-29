from pathlib import Path
import json

CONF_FILE = f"{Path(__file__).parent.absolute()}/config.json"

default_conf = '{"Initiatives":{}, "Settings":{}, "Keybinds":{}}'
default_ini = {"initiative": 0, "ignore": False, "lastload": 0}
default_settings = {"on_top_settings": False}
default_keybinds = {"next": "f2", "previous": "f3"}

ini_keys = {"initiative", "ignore", "lastload"}
keybinds_keys = {"next", "previous"}


class ConfManager:
    @staticmethod
    def get_json() -> json:
        content = None
        try:
            with open(CONF_FILE, "r") as cf:
                content = json.load(cf)
        except FileNotFoundError:
            with open(CONF_FILE, "x") as cf:
                cf.write(default_conf)
        except Exception as e:
            print("Error", e)
        finally:
            if not content:
                content = json.loads(default_conf)
        return content

    @staticmethod
    def get_characters() -> list:
        try:
            characters = ConfManager.get_json()["Initiatives"]

        except KeyError:
            characters = {}
            ConfManager.__save_initiative(characters)

        res = []
        for character in characters.keys():
            if " " in character:
                continue
            lastload = (
                characters[character]["lastload"]
                if "lastload" in characters[character]
                else 0
            )
            res.append((character, lastload))

        return res

    # Initiative methods

    @staticmethod
    def get_initiative(character: str) -> dict:
        try:
            initiative = ConfManager.get_json()["Initiatives"]

        except KeyError:
            initiative = {}

        character_name = character
        if character_name not in initiative:
            initiative[character_name] = default_ini

        if not ini_keys.issubset(initiative[character_name].keys()):
            initiative[character_name] = default_ini

        if (
            not isinstance(initiative[character_name]["initiative"], int)
            or not isinstance(initiative[character_name]["ignore"], bool)
            or not isinstance(initiative[character_name]["lastload"], int)
        ):
            initiative[character_name] = default_ini

        ConfManager.__save_initiative(initiative)

        return initiative

    @staticmethod
    def set_initiative(values):
        initiative = ConfManager.get_json()["Initiatives"]
        for key, value in values.items():
            if key not in initiative.keys():
                # remove added numbers of multiple windows with the same name
                key = "".join([c for c in key if not c.isdigit()])

            if "Dofus" in key:
                key = key[:9]

            for k, v in value.items():
                match k:
                    case "initiative":
                        try:
                            v = int(v)
                        except:
                            v = 0

                        initiative[key]["initiative"] = v
                    case "ignore":
                        try:
                            v = bool(v)
                        except:
                            v = False
                        initiative[key]["ignore"] = v
                    case "lastload":
                        try:
                            v = int(v)
                        except:
                            v = 0
                        initiative[key]["lastload"] = v
                    case _:
                        print(f"Unknown key: {k}")

        ConfManager.__save_initiative(initiative)

    @staticmethod
    def __save_initiative(initiative):
        config = ConfManager.get_json()
        config["Initiatives"] = initiative
        with open(CONF_FILE, "w") as cf:
            json.dump(config, cf)

    # Settings methods

    @staticmethod
    def get_settings():
        try:
            settings = ConfManager.get_json()["Settings"]
            if settings == {}:
                raise KeyError

        except KeyError:
            settings = default_settings
            ConfManager.__save_settings(settings)

        return settings

    @staticmethod
    def set_settings(values):
        settings = ConfManager.get_json()["Settings"]
        for key, value in values.items():
            settings[key] = value

        ConfManager.__save_settings(settings)

    @staticmethod
    def __save_settings(settings):
        config = ConfManager.get_json()
        config["Settings"] = settings
        with open(CONF_FILE, "w") as cf:
            json.dump(config, cf)

    # Keybinds methods
    @staticmethod
    def get_keybinds():
        try:
            keybinds = ConfManager.get_json()["Keybinds"]
            if keybinds == {}:
                raise KeyError
            if not keybinds_keys.issubset(keybinds.keys()):
                raise KeyError

        except KeyError:
            keybinds = default_keybinds
            ConfManager.__save_keybinds(keybinds)

        return keybinds

    @staticmethod
    def set_keybinds(values):
        keybinds = ConfManager.get_json()["Keybinds"]
        for key, value in values.items():
            keybinds[key] = value

        ConfManager.__save_keybinds(keybinds)

    @staticmethod
    def __save_keybinds(keybinds):
        config = ConfManager.get_json()
        config["Keybinds"] = keybinds
        with open(CONF_FILE, "w") as cf:
            json.dump(config, cf)
