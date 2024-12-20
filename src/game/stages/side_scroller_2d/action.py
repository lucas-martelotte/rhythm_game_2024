from pygame.event import Event

from src.core.entity import Camera

from .game_object import GameObject


class Action:

    def __init__(self):
        self.started = False

    def start(self, game_objects: dict[str, GameObject], camera: Camera):
        self.mc = game_objects["mc"]
        self.game_objs = game_objects
        self.camera = camera
        self.started = True

    def on_event(self, event: Event):
        if not self.started:
            raise Exception("Must call start() first.")

    def done(self) -> bool:
        return False
