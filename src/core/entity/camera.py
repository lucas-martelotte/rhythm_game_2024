from pygame.surface import Surface

from src.core.essentials import FPos, Pos

from .entity import Entity, RenderableEntity


class Camera(Entity):
    def __init__(self, position: Pos | None = None, offset: Pos | None = None):
        super().__init__(position or Pos(0, 0))
        self.target_pos: FPos | None = None
        self.offset = offset or Pos(0, 0)

    def update(self):
        super().update()
        if self.target_pos:
            dist_to_target = FPos.dist_squared(self.target_pos, self.fpos)
            if dist_to_target < 1:
                self.fpos = self.target_pos
                self.target_pos = None
            else:
                self.vel = self.target_pos - self.fpos

    def render(self, screen: Surface, game_obj: RenderableEntity):
        game_obj.render(screen, origin=self.pos + self.offset)
