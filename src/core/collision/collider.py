import numpy as np

from src.core.essentials import FPos, Pos, Rect

from .gjk import gjk_algorithm
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

    @property
    def polys(self) -> list[ConvexPolygon]:
        return self._polys

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

    def collide(self, collider: "Collider", pos: FPos) -> FPos | None:
        """
        Receives a collider and its position. For each polygon in both
        colliders the algorithm translates the (other) polygon by that
        position and runs the GJK algorithm to determine the collision
        with self. If any of these polygons collide, returns their mdv
        """
        for poly1 in self.polys:
            for poly2 in collider.polys:
                mdv = gjk_algorithm(poly1.points, poly2.points + pos.to_array())
                if mdv is not None:
                    return FPos(mdv[0], mdv[1])
        return None


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
