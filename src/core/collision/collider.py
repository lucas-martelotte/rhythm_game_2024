import numpy as np

from src.core.essentials import Pos, Rect

from .poly import ConvexPolygon


class Collider:  # Polygon collider
    def __init__(self, polys: list[ConvexPolygon]):
        """
        The position of each polygon is relative, i.e. the origin
        will always be considered equal to pos.
        """
        self._polys = polys
        self._bounding_rect = self._calculate_bounding_rect()
        self._convex_hull = ConvexPolygon(np.vstack([p.points for p in polys]))

    def get_polygons(self) -> list[np.ndarray]:
        return [p.points for p in self._polys]

    def _calculate_bounding_rect(self) -> Rect:
        left = min(np.min(poly.points[:, 0]) for poly in self._polys)
        right = max(np.max(poly.points[:, 0]) for poly in self._polys)
        top = min(np.min(poly.points[:, 1]) for poly in self._polys)
        bottom = max(np.max(poly.points[:, 1]) for poly in self._polys)
        return Rect(int(left), int(top), int(right - left), int(bottom - top))

    @property
    def bounding_rect(self) -> Rect:
        return self._bounding_rect

    @property
    def convex_hull(self) -> np.ndarray:
        return self._convex_hull.points

    def point_collision(self, vector: Pos) -> bool:
        arr = vector.to_array()
        return any(p.point_collision(arr) for p in self._polys)


class RectCollider(Collider):
    # fmt: off
    def __init__(self, rect: Rect):
        self.rect = rect
        super().__init__(
            [ConvexPolygon(np.array([
                [rect.left, rect.top], 
                [rect.right, rect.top], 
                [rect.right, rect.bottom], 
                [rect.left, rect.bottom], 
            ]),
            ordered=True)]
        )
    # fmt: on
