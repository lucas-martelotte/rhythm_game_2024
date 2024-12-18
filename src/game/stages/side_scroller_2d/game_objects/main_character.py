import pygame
from pygame.event import Event
from pygame.surface import Surface

from src.core.collision import RectCollider
from src.core.entity import Sprite, SpriteFrame
from src.core.essentials import Anchor, FPos, Pos, Rect

from ..game_object import GameObject
from ..trigger import TriggerSheet


class MainCharacter(GameObject):
    # fmt: off
    def __init__(self, position: Pos):
        super().__init__(
            "mc",
            position,
            Sprite(
                state_machine={"idle": "idle"},
                sprite_sheet={"idle": [SpriteFrame(
                    Surface((50, 100)),
                    RectCollider(Rect(0, -100, 50, 100)),
                    Anchor.BOTTOMLEFT
                )]},
                initial_state="idle",
                fps=1
            ),
            TriggerSheet(),
            collidable=True,
            interactable=True
        )
        self.falling = False
        self.speed = 300
        self.gravity = 600
    # fmt: on

    def update(self):
        super().update()
        self.acc = FPos(0, self.gravity) if self.falling else FPos(0, 0)
        if not self.walking and not self.falling:  # friction
            self.acc = FPos(-10 * self.vel.x, 0)

    def on_event(self, event: Event):
        super().on_event(event)
        pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.vel.x = -self.speed
            if event.key == pygame.K_RIGHT:
                self.vel.x = self.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and pressed[pygame.K_LEFT]:
                self.vel.x = -self.speed
            if event.key == pygame.K_LEFT and pressed[pygame.K_RIGHT]:
                self.vel.x = self.speed

    @property
    def walking(self) -> bool:
        pressed = pygame.key.get_pressed()
        return pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]
