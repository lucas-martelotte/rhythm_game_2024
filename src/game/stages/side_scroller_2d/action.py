from pygame.event import Event

from src.core.entity import Camera

from .game_object import GameObject
from .game_objects import DialogueBox, MainCharacter


class Action:

    def __init__(self):
        self.__running = False

    def start(self, game_objects: dict[str, GameObject], camera: Camera):
        mc = game_objects["mc"]
        assert isinstance(mc, MainCharacter)
        self.mc = mc

        dialogue_box = game_objects["dialogue_box"]
        assert isinstance(dialogue_box, DialogueBox)
        self.dialogue_box = dialogue_box

        self.game_objs = game_objects
        self.camera = camera
        self.__running = True

    def finish(self):
        self.__running = False

    def on_event(self, event: Event):
        if not self.__running:
            raise Exception("Must call start() first.")

    @property
    def done(self) -> bool:
        return not self.__running
