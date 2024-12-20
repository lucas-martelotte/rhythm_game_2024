from pygame.event import Event

from src.core.entity import Camera

from .game_object import GameObject
from .game_objects import DialogueBox, MainCharacter


class Action:

    def __init__(self):
        self._started = False
        self._done = False

    def start(self, game_objects: dict[str, GameObject], camera: Camera):
        mc = game_objects["mc"]
        assert isinstance(mc, MainCharacter)
        self.mc = mc

        dialogue_box = game_objects["dialogue_box"]
        assert isinstance(dialogue_box, DialogueBox)
        self.dialogue_box = dialogue_box

        self.game_objs = game_objects
        self.camera = camera
        self._started = True
        self._done = False

    def on_event(self, event: Event):
        if not self._started:
            raise Exception("Must call start() first.")

    @property
    def done(self) -> bool:
        return self._done
