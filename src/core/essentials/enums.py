from enum import Enum, IntEnum, auto


class MouseButtons(IntEnum):
    """Numbers are specific to match with the pygame convention"""

    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5


class Anchor(Enum):
    TOPRIGHT = auto()
    MIDRIGHT = auto()
    BOTTOMRIGHT = auto()
    TOPLEFT = auto()
    MIDLEFT = auto()
    BOTTOMLEFT = auto()
    CENTER = auto()
    MIDTOP = auto()
    MIDBOTTOM = auto()


class SceneTransitionState(Enum):
    IDLE = auto()  # No scene transition required
    CLOSE_AND_MOVE_TO_EXISTING_SCENE = auto()
    CLOSE_AND_MOVE_TO_NEW_SCENE = auto()
    MOVE_TO_EXISTING_SCENE = auto()
    MOVE_TO_NEW_SCENE = auto()
