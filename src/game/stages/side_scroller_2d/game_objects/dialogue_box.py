import pygame
from pygame.surface import Surface

from src.core.entity import BasicSprite, RenderableEntity
from src.core.essentials import Anchor, FPos, FPSTracker, Pos
from src.core.gui import Textbox
from src.game.singletons import Mixer

from ..game_object import GameObject


class DialogueBox(GameObject):
    # fmt: off
    def __init__(
        self,
        size: tuple[int, int], 
        characters_per_second: int = 24
    ):
        sfc = Surface((size[0], size[1] + 20)).convert_alpha()
        sfc.fill((0, 0, 0, 0))
        pygame.draw.rect(sfc, (0,0,0), (0, 0, size[0], size[1]))
        pygame.draw.polygon(sfc, (0,0,0), [(0,size[1]), (0, size[1]+20), (20, size[1])])

        super().__init__(
            "dialogue_box", 
            Pos(0, 0),
            BasicSprite(sfc, Anchor.BOTTOMLEFT)
        )

        self.textbox = Textbox(size, text_color=(255, 255, 255), padding=(20, 10))
        self.fps_tracker = FPSTracker(characters_per_second)
        self.fps = characters_per_second
        self.sprite.hidden = True
        self._target_obj: RenderableEntity | None = None

        self._text_to_display = ""
        self._blip_sound: str | None = None
    # fmt: on

    def update(self):
        super().update()
        if self._target_obj:
            rect = self._target_obj.get_curr_rect()
            self.fpos = FPos.from_pos(rect.top_right) + FPos(0, -10)
        chars_displayed = len(self.textbox.text)
        chars_left = len(self._text_to_display) - chars_displayed
        frames_passed = self.fps_tracker.get_frames_passed()
        if chars_left > 0:
            if frames_passed > 0 and self._blip_sound:
                Mixer().play_blip(self._blip_sound)
            chars_to_display = min(frames_passed, chars_left)
            start, end = chars_displayed, chars_displayed + chars_to_display
            self.textbox.text = self.textbox.text + self._text_to_display[start:end]

    def render(self, screen: Surface, origin: Pos | None = None):
        origin = origin or Pos(0, 0)
        super().render(screen, origin=origin)
        if not self.get_hidden():
            rect = self.get_curr_rect(origin=origin)
            screen.blit(self.textbox.get_sfc(), (rect.x, rect.y))
            if self.all_text_is_displayed():
                # fmt: off
                pygame.draw.polygon(screen, (255, 255, 255), [
                    (rect.right - 30, rect.bottom - 70),
                    (rect.right - 30, rect.bottom - 30),
                    (rect.right - 10, rect.bottom - 50)
                ])
                # fmt: on

    def set_target_obj(self, target_obj: GameObject):
        self._target_obj = target_obj

    def set_text(self, text: str, blip_sound: str | None = None):
        self._text_to_display = text
        self._blip_sound = blip_sound
        self.textbox.text = ""
        self.sprite.hidden = False

    def all_text_is_displayed(self) -> bool:
        return len(self._text_to_display) - len(self.textbox.text) == 0

    def display_all_text(self):
        self.textbox.text = self._text_to_display
