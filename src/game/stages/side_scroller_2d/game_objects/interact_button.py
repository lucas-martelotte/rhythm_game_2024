from pygame.surface import Surface

from src.core.entity import BasicSprite, Sprite
from src.core.essentials import Anchor, FPos, Pos

from ..game_object import GameObject


class InteractButtonSprite(BasicSprite):
    def __init__(self):
        super().__init__(Surface((50, 50)), Anchor.MIDBOTTOM)
        self.hidden = True


class InteractButton(GameObject):
    # fmt: off
    def __init__(self) -> None:
        self._interacting_obj: GameObject | None = None
        super().__init__(
            "interact_button",
            Pos(0,0),
            InteractButtonSprite(),
            z_index=10
        )
    # fmt: on

    def set_interactable_obj(self, int_obj: GameObject | None):
        self._interacting_obj = int_obj
        if int_obj:
            obj_rect = int_obj.get_curr_rect()
            self.fpos = FPos(obj_rect.x_middle, obj_rect.y - 20)
            self.sprite.hidden = False
        else:
            self.sprite.hidden = True

    @property
    def interacting_obj(self) -> GameObject | None:
        return self._interacting_obj
