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
            collidable=False,
            interactable=False
        )
        self.falling = False
        self.walk_speed = 600
        self.jump_speed = 1500
        self.gravity = 4000
    # fmt: on

    def update(self):
        super().update()
        if self.falling:
            self.acc = FPos(0, self.gravity)
        else:
            self.acc = FPos(0, 0)
            self.vel.y = 0
        self.vel.x = 0 if abs(self.vel.x) < 1 else self.vel.x
        if not self.walking and not self.falling:
            self.acc = FPos(-10 * self.vel.x, 0)
        if not self.walking and self.falling:
            self.vel.x = 0

    def on_event(self, event: Event):
        super().on_event(event)
        pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.vel.x = -self.walk_speed
            if event.key == pygame.K_RIGHT:
                self.vel.x = self.walk_speed
            if event.key in {pygame.K_UP, pygame.K_SPACE} and not self.falling:
                self.vel.y = -self.jump_speed
                self.falling = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and pressed[pygame.K_LEFT]:
                self.vel.x = -self.walk_speed
            if event.key == pygame.K_LEFT and pressed[pygame.K_RIGHT]:
                self.vel.x = self.walk_speed

    @property
    def walking(self) -> bool:
        pressed = pygame.key.get_pressed()
        return pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]
