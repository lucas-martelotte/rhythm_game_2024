import pygame
from pygame.surface import Surface

from src.core.entity import BasicSprite
from src.core.essentials import Anchor, FPos, Pos
from src.game.stages.side_scroller_2d import (
    GameObject,
    MainCharacter,
    MainScene,
    Trigger,
    TriggerSheet,
)
from src.game.stages.side_scroller_2d.actions import DialogueAction

# fmt: off
# ============================= #
# ========== Sprites ========== #
# ============================= #
ground1_sprite = BasicSprite(
    Surface((1440, 80)), 
    Anchor.TOPLEFT, 
    collider_offset=Pos(0, 1)
)
ground1_sprite.sfc.fill((0, 100, 50))
ground1 = GameObject(
    "ground1", 
    Pos(0, 1000), 
    ground1_sprite,
    collidable=True,
    interactable=False
)


ground2_sprite = BasicSprite(
    Surface((800, 200)), 
    Anchor.TOPLEFT, 
    collider_offset=Pos(0, 1)
)
ground2_sprite.sfc.fill((100, 100, 100))
ground2 = GameObject(
    "ground2", 
    Pos(640, 880), 
    ground2_sprite,
    collidable=True,
    interactable=False
)


ground3_sprite = BasicSprite(
    Surface((200, 800)), 
    Anchor.TOPLEFT, 
    collider_offset=Pos(0, 1)
)
ground3_sprite.sfc.fill((80, 80, 80))
ground3 = GameObject(
    "ground3", 
    Pos(1240, 280), 
    ground3_sprite,
    collidable=True,
    interactable=False
)

interactable1_sprite = BasicSprite(
    Surface((80, 200)), 
    Anchor.BOTTOMLEFT
)
interactable1_sprite.sfc.fill((255, 0, 0))
interactable1 = GameObject(
    "interactable1", 
    Pos(100, 1000), 
    interactable1_sprite,
    collidable=False,
    interactable=True
)

# ============================= #
# ============================= #
# ============================= #
# fmt: on


class TestMainScene1(MainScene):
    def __init__(self):
        # fmt: off
        super().__init__(
            "test_main_scene_1",
            MainCharacter(Pos(0, 1000)),
            {ground1, ground2, ground3, interactable1},
            TriggerSheet(
                [], 
                {
                    ("interactable1", "A") : {
                        Trigger(set(), [
                            DialogueAction("Objeto doidao", "mc", "blip_male.opus"),
                            DialogueAction("Doidao mrm", "mc", "blip_male.opus"),
                        ])
                    }
                }
            ),
        )
        # fmt: on
