from pygame.event import Event
from pygame.surface import Surface

from src.core.entity import RenderableEntity, Sprite
from src.core.essentials import Pos


class GameObject(RenderableEntity):
    def __init__(
        self,
        name: str,
        position: Pos,
        sprite: Sprite,
        collidable: bool = False,
        interactable: bool = False,
        z_index: int = 1,
    ):
        super().__init__(sprite, position)
        self.name = name
        self.collidable = collidable
        self.interactable = interactable
        self.z_index = z_index
        self.local_switch = "A"

    def update(self):
        super().update()

    def on_event(self, event: Event):
        super().on_event(event)

    def set_hidden(self, hidden: bool):
        self.sprite.hidden = hidden

    def get_hidden(self) -> bool:
        return self.sprite.hidden
