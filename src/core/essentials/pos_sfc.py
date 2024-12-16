from pygame.surface import Surface

from .enums import Anchor
from .pos import Pos


class PosSurface:
    def __init__(self, surface: Surface, position: Pos, anchor: Anchor):
        self.sfc = surface
        self.pos = position
        self.anchor = anchor

    def render(self, screen: Surface):
        rect = self.sfc.get_rect(**{self.anchor.name.lower(): self.pos.to_tuple()})
        screen.blit(self.sfc, rect)

    def move(self, delta: Pos) -> "PosSurface":
        return PosSurface(self.sfc, self.pos + delta, self.anchor)
