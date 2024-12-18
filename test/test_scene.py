import pygame
from pygame.surface import Surface

from src.core.essentials import Anchor, MouseButtons, Scene
from src.core.gui import BasicButton, Textbox
from src.game.singletons import GameSettings, Mixer, Mouse


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
                "pressed": [color_sfc((0, 0, 0)), color_sfc((100, 255, 100))] * 10,
            },
            {("pressed", 0): "click.mp3", ("selected_ini", 0): "select.ogg"},
            anchor=Anchor.CENTER,
        )
        self.textbox = Textbox(
            (200, 100),
            text="Here we have a sample text. This is a very cool text and serves the purpose of testing the textbox dimensions.",
        )

    def update(self):
        self.button.update()
        self.button.handle_mouse_hover(Mouse().get_pos())

    def render(self, screen: Surface):
        screen.fill((255, 255, 255))
        self.button.render(screen)
        if audio := self.button.sprite.pop_audio():
            Mixer().play_sfx(audio)
        screen.blit(self.textbox.get_sfc(), (0, 0))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MouseButtons.LEFT:
                self.button.handle_mouse_press(Mouse().get_pos())
