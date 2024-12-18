from pygame.surface import Surface

from src.core.entity import Entity
from src.core.essentials import Pos

from .game_object import GameObject


class Camera(Entity):
    def __init__(self, position: Pos = Pos(0, 0)):
        super().__init__(position)

    def render(self, screen: Surface, game_obj: GameObject):
        game_obj.render(screen, origin=self.pos)
