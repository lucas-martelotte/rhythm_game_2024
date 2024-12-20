from pygame.surface import Surface

from src.core.essentials import FPos, Pos

from .entity import Entity, RenderableEntity


class Camera(Entity):
    def __init__(self, position: Pos | None = None, offset: Pos | None = None):
        super().__init__(position or Pos(0, 0))
        self.target_obj: Entity | None = None
        self.offset = offset or Pos(0, 0)

    def update(self):
        super().update()
        if self.target_obj:
            target_fpos = self.target_obj.fpos
            dist_to_target = FPos.dist_squared(target_fpos, self.fpos)
            if dist_to_target < 1:
                self.fpos = target_fpos
                self.vel = FPos(0, 0)
            else:
                self.vel = target_fpos - self.fpos

    def render(self, screen: Surface, game_obj: RenderableEntity):
        game_obj.render(screen, origin=self.origin)

    @property
    def origin(self) -> Pos:
        return self.pos + self.offset
