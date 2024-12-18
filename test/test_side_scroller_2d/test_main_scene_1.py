from src.core.essentials import Pos
from src.game.stages.side_scroller_2d import MainCharacter, MainScene


class TestMainScene1(MainScene):
    def __init__(self):
        super().__init__("test_main_scene_1", MainCharacter(Pos(0, 500)), {})
