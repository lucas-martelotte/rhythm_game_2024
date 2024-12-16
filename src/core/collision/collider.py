from src.core.essentials import Pos, Rect


class Collider:
    def point_collision(self, vector: Pos) -> bool:
        return False


class RectCollider(Collider):
    def __init__(self, rect: Rect):
        self.rect = rect
        super().__init__()

    def point_collision(self, vector: Pos) -> bool:
        return (
            self.rect.left <= vector.x <= self.rect.right
            and self.rect.top <= vector.y <= self.rect.bottom
        )
