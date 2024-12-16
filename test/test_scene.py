import pygame
from pygame.surface import Surface

from src.core.essentials import Anchor, MouseButtons, Scene
from src.core.gui import BasicButton
from src.game.singletons import GameSettings, Mouse


class TestScene(Scene):
    def __init__(self):
        super().__init__("test")
        settings = GameSettings()

        def color_sfc(color: tuple[int, int, int]):
            sfc = Surface((200, 100))
            sfc.fill(color)
            return sfc

        self.button = BasicButton(
            settings.screen_center(),
            {
                "idle": [color_sfc((100, 100, 100))],
                "selected_ini": [color_sfc((255, 100, 100))] * 5,
                "selected": [color_sfc((100, 255, 100))],
                "pressed": [color_sfc((255, 100, 100)), color_sfc((100, 255, 100))]
                * 10,
            },
            {},
            anchor=Anchor.CENTER,
        )

    def update(self, frames_passed: int):
        self.button.update(frames_passed)
        self.button.handle_mouse_hover(Mouse().get_pos())

    def render(self, screen: Surface):
        screen.fill((255, 255, 255))
        self.button.get_sfc().render(screen)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MouseButtons.LEFT:
                self.button.handle_mouse_press(Mouse().get_pos())
