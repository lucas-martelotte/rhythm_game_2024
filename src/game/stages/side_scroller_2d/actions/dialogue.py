import pygame

from src.core.entity import Camera
from src.core.essentials import MouseButtons

from ..action import Action
from ..game_object import GameObject


class DialogueAction(Action):
    def __init__(self, text: str, speaker: str, blip_sound: str | None = None):
        super().__init__()
        self.text = text
        self.speaker = speaker
        self.blip_sound = blip_sound

    def start(self, game_objects: dict[str, GameObject], camera: Camera):
        super().start(game_objects, camera)
        self.dialogue_box.set_target_obj(self.game_objs[self.speaker])
        self.dialogue_box.set_text(self.text, blip_sound=self.blip_sound)
        self.dialogue_box.set_hidden(False)

    def on_event(self, event):
        super().on_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self._press_dialogue_box()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MouseButtons.LEFT:
                self._press_dialogue_box()

    def _press_dialogue_box(self):
        if self.dialogue_box.all_text_is_displayed():
            self.finish()
            return
        self.dialogue_box.display_all_text()
