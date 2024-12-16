import json

from src.core.essentials import Pos
from src.core.utils import SingletonMetaclass


class GameSettings(metaclass=SingletonMetaclass):

    GAME_SETTINGS_PATH = "./src/data/meta/config/game_settings.json"

    def __init__(self):
        with open(self.GAME_SETTINGS_PATH, "r") as f:
            config_dict = json.loads(f.read())
            self.display_width = int(config_dict["width"])
            self.display_height = int(config_dict["height"])
            self.fps = int(config_dict["fps"])
            self.fullscreen = config_dict["display"] == "fullscreen"

    def display_center(self) -> Pos:
        return Pos(self.display_width // 2, self.display_height // 2)

    def display_size(self) -> tuple[int, int]:
        return self.display_width, self.display_height

    def screen_size(self) -> tuple[int, int]:
        return 1440, 1080

    def screen_center(self) -> Pos:
        return Pos(720, 540)
