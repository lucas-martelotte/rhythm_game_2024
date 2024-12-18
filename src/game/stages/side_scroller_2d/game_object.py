from pygame.event import Event
from pygame.surface import Surface

from src.core.entity import RenderableEntity, Sprite
from src.core.essentials import Pos

from .trigger import TriggerSheet


class GameObject(RenderableEntity):
    def __init__(
        self,
        name: str,
        position: Pos,
        sprite: Sprite,
        trigger_sheet: TriggerSheet,
        collidable: bool = False,
        interactable: bool = False,
    ):
        super().__init__(sprite, position)
        self.name = name
        self.trigger_sheet = trigger_sheet
        self.collidable = collidable
        self.interactable = interactable

    def update(self):
        super().update()

    def on_event(self, event: Event):
        super().on_event(event)

    def render(self, screen: Surface, origin: Pos = Pos(0, 0)):
        super().render(screen)
