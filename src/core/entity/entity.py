from pygame.event import Event
from pygame.surface import Surface

from src.core.essentials import FPos, Pos, TimeTracker
from src.core.utils import sgn_round

from .sprite import Sprite


class Entity(TimeTracker):
    def __init__(self, position: Pos):
        super().__init__()
        self.fpos = FPos.from_pos(position)
        self.vel = FPos(0, 0)  # pixels per second
        self.acc = FPos(0, 0)

    def update(self):
        t = self.get_time_passed()
        self.fpos += self.vel * t
        self.vel += self.acc * t

    def on_event(self, event: Event):
        pass

    @property
    def pos(self) -> Pos:
        return self.fpos.round()


class RenderableEntity(Entity):
    def __init__(self, sprite: Sprite, position: Pos):
        super().__init__(position)
        self.sprite = sprite

    def update(self):
        super().update()
        self.sprite.update()

    def render(self, screen: Surface, origin: Pos | None = None):
        origin = origin or Pos(0, 0)
        frame = self.sprite.get_curr_sprite()
        global_pos = self.pos - origin
        rect = frame.sfc.get_rect(**{frame.anchor.name.lower(): global_pos.to_tuple()})
        screen.blit(frame.sfc, rect)

    def point_collision(self, vector: Pos) -> bool:
        return self.sprite.get_curr_sprite().collider.point_collision(vector - self.pos)

    def collide(
        self, entity: "RenderableEntity", offset: FPos = FPos(0, 0)
    ) -> FPos | None:
        col1 = self.sprite.get_curr_sprite().collider
        col2 = entity.sprite.get_curr_sprite().collider
        col2_pos = entity.fpos - self.fpos + offset
        return col1.collide(col2, col2_pos)
