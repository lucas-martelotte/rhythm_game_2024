from math import pi

import pygame
from numpy import zeros
from pygame.event import Event
from pygame.surface import Surface

from src.core.collision import RectCollider, polar_angle
from src.core.entity import Sprite, SpriteFrame
from src.core.essentials import Anchor, FPos, Pos, Rect

from ..game_object import GameObject


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
            collidable=False,
            interactable=False
        )
        self.falling = False
        self.walk_speed = 600
        self.jump_speed = 1500
        self.gravity = 4000
        self.friction_factor = 50
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
            self.acc = FPos(-self.friction_factor * self.vel.x, 0)
        if not self.walking and self.falling:
            self.vel.x = 0

    def on_event(self, event: Event):
        super().on_event(event)
        pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.vel.x = -self.walk_speed
                self.acc.x = 0
            if event.key == pygame.K_RIGHT:
                self.vel.x = self.walk_speed
                self.acc.x = 0
            if event.key in {pygame.K_UP, pygame.K_SPACE} and not self.falling:
                self.vel.y = -self.jump_speed
                self.falling = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and pressed[pygame.K_LEFT]:
                self.vel.x = -self.walk_speed
            if event.key == pygame.K_LEFT and pressed[pygame.K_RIGHT]:
                self.vel.x = self.walk_speed

    def handle_collisions(self, collidables: set[GameObject]):
        for game_obj in collidables:
            if mdv := self.collide(game_obj):
                self.fpos -= mdv * 1.0001
                v_angle = polar_angle(zeros(2), mdv.to_array())
                if -pi / 4 > v_angle > -3 * pi / 4:
                    self.falling = False
        # Check if mc still on ground
        if not any(self.collide(o, offset=FPos(0, -10)) for o in collidables):
            self.falling = True

    @property
    def walking(self) -> bool:
        pressed = pygame.key.get_pressed()
        return pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]
