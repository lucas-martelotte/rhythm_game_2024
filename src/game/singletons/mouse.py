import json

from pygame.mouse import get_pos, get_pressed

from src.core.essentials import MouseButtons, Pos
from src.core.utils import SingletonMetaclass

from .game_settings import GameSettings


class Mouse(metaclass=SingletonMetaclass):
    def get_pos(self) -> Pos:
        settings = GameSettings()
        dw, dh = settings.display_size()
        sw, sh = settings.screen_size()
        x, y = get_pos()
        return Pos.from_tuple(((x * sw) // dw, (y * sh) // dh))

    def is_pressed(self, btn: MouseButtons) -> bool:
        return get_pressed(num_buttons=5)[btn - 1]
