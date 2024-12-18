from pygame.event import Event
from pygame.surface import Surface

from src.core.essentials import Pos, Scene

from .game_object import GameObject
from .game_objects import MainCharacter


class MainScene(Scene):
    def __init__(
        self, name: str, mc: MainCharacter, game_objects: dict[str, GameObject]
    ):
        super().__init__(name)
        self.game_objs = game_objects
        self.game_objs["mc"] = mc
        self.mc = mc

    def update(self):
        super().update()
        for game_obj in self.game_objs.values():
            game_obj.update()
        pass

    def on_event(self, event: Event):
        super().on_event(event)
        for game_obj in self.game_objs.values():
            game_obj.on_event(event)

    def render(self, screen: Surface):
        super().render(screen)
        screen.fill((255, 255, 255))
        for game_obj in self.game_objs.values():
            game_obj.render(screen)
