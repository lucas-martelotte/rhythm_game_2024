import numpy as np


class Pos:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    @staticmethod
    def from_tuple(pos: tuple[int, int]) -> "Pos":
        return Pos(pos[0], pos[1])

    @staticmethod
    def convex_combination(pos1: "Pos", pos2: "Pos", t: float) -> "Pos":
        assert 0 <= t <= 1
        x = int(pos1.x * t + (1 - t) * pos2.x)
        y = int(pos1.y * t + (1 - t) * pos2.y)
        return Pos(x, y)

    def to_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    def to_array(self) -> np.ndarray:
        return np.array([self.x, self.y])

    def __add__(self, other: object) -> "Pos":
        assert isinstance(other, Pos)
        return Pos(self.x + other.x, self.y + other.y)

    def __mul__(self, other: object) -> "Pos":  # scalar multiplication
        assert isinstance(other, int)
        return Pos(self.x * other, self.y * other)

    def inv(self) -> "Pos":
        return self * (-1)

    def __sub__(self, other: object) -> "Pos":
        assert isinstance(other, Pos)
        return self + other.inv()

    def dot(self, other: "Pos") -> int:
        return self.x * other.x + self.y * other.y

    def norm_square(self) -> int:
        return self.dot(self)

    def dist_squared(self, other: "Pos") -> int:
        return Pos.norm_square(other - self)


class FPos:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def round(self) -> Pos:
        return Pos(int(self.x), int(self.y))

    @staticmethod
    def from_pos(pos: Pos) -> "FPos":
        return FPos(pos.x, pos.y)

    @staticmethod
    def from_tuple(pos: tuple[int, int]) -> "FPos":
        return FPos(pos[0], pos[1])

    @staticmethod
    def convex_combination(pos1: "FPos", pos2: "FPos", t: float) -> "FPos":
        assert 0 <= t <= 1
        x = int(pos1.x * t + (1 - t) * pos2.x)
        y = int(pos1.y * t + (1 - t) * pos2.y)
        return FPos(x, y)

    def to_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def to_array(self) -> np.ndarray:
        return np.array([self.x, self.y])

    def __add__(self, other: object) -> "FPos":
        assert isinstance(other, FPos)
        return FPos(self.x + other.x, self.y + other.y)

    def __mul__(self, other: object) -> "FPos":  # scalar multiplication
        assert isinstance(other, (int, float))
        return FPos(self.x * other, self.y * other)

    def inv(self) -> "FPos":
        return self * (-1)

    def __sub__(self, other: object) -> "FPos":
        assert isinstance(other, FPos)
        return self + other.inv()

    def dot(self, other: "FPos") -> float:
        return self.x * other.x + self.y * other.y

    def norm_square(self) -> float:
        return self.dot(self)

    def dist_squared(self, other: "FPos") -> float:
        return FPos.norm_square(other - self)
