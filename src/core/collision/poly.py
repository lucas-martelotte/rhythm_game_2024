from math import atan2, pi

import numpy as np


def orientation(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray):
    """
    Receives three 2 x 1 vectors as input.
    Returns if the orientation of the segments (p1, p2) -> (p2, p3)
    follows a clockwise (1), counter-clockwise (-1) or straight (0)
    trajectory.
    """
    x1, y1, x2, y2, x3, y3 = p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]
    d = (y3 - y2) * (x2 - x1) - (y2 - y1) * (x3 - x2)
    if d > 0:
        return 1
    elif d < 0:
        return -1
    else:
        return 0


def polar_angle(p1: np.ndarray, p2: np.ndarray) -> float:
    """
    Receives two 2x1 vectors as input and returns the angle
    between the x-axis and the line (p1, p2).
    """
    x1, x2, y1, y2 = p1[0], p2[0], p1[1], p2[1]
    if y1 == y2:
        if x1 == x2:
            return 0
        return -pi
    dy, dx = y1 - y2, x1 - x2
    return atan2(dy, dx)


def graham_scan(points: np.ndarray) -> np.ndarray:
    """Returns the convex hull of the input points, ordered anticlockwise"""
    p0 = min(points, key=lambda p: (p[1], p[0]))
    point_list = list(points)
    point_list.sort(key=lambda p: (polar_angle(p0, p), np.linalg.norm(p0 - p)))
    hull: list[np.ndarray] = []
    for i in range(len(point_list)):
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], point_list[i]) != 1:
            hull.pop()
        hull.append(point_list[i])
    return np.array(hull)


class ConvexPolygon:
    def __init__(self, points: np.ndarray, ordered=False):
        points_shape = np.shape(points)
        assert len(points_shape) == 2 and points_shape[1] == 2
        self.n_points = points_shape[0]
        self.points = points if ordered else graham_scan(points)

    def point_collision(self, vector: np.ndarray) -> bool:
        """
        Applies the Raycasting algorithm: it receives a point
        (a numpy array of size 2) and returns if the point lies
        inside the polygon.
        """
        intersections, x, y, n = 0, vector[0], vector[1], self.n_points
        for i in range(n):
            p1, p2 = self.points[i], self.points[(i + 1) % n]
            if (y < p1[1]) != (y < p2[1]) and (
                x < (p2[0] - p1[0]) * (p2[1] - p1[1]) + p1[0]
            ):
                intersections += 1
        return intersections % 2 == 1
