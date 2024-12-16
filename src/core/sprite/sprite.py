from pygame.surface import Surface

from src.core.collision import Collider
from src.core.essentials import Pos, PosSurface


class SpriteFrame:
    def __init__(
        self, surface: PosSurface, collider: Collider, audio: str | None = None
    ):
        self.sfc = surface  # relative_pos
        self.collider = collider  # relative_pos
        self.audio = audio


class Sprite:
    def __init__(
        self,
        state_machine: dict[str, str],
        sprite_sheet: dict[str, list[SpriteFrame]],
        position: Pos,
        initial_state: str,
    ):
        self._state_machine = state_machine
        self._sprite_sheet = sprite_sheet
        self._frame = 0
        self.pos = position
        self.state = initial_state
        self._audio_to_play: str | None = None  # handle frame loss

    def update(self, frames_passed: int):
        for _ in range(frames_passed):
            self._frame += 1
            while self._frame >= self.get_curr_max_frames():
                self._frame -= self.get_curr_max_frames()
                self.state = self._state_machine[self.state]
            self._audio_to_play = self.get_curr_sprite().audio or self._audio_to_play

    def point_collision(self, vector: Pos) -> bool:
        return self.get_curr_sprite().collider.point_collision(vector - self.pos)

    def set_state(self, state: str, force_reset=False):
        if self.state != state or force_reset:
            self._frame = -1  # need to do this to trigger frame 0
        self.state = state
        self.update(1)

    def get_sfc(self) -> PosSurface:
        return self.get_curr_sprite().sfc.move(self.pos)

    def pop_audio(self) -> str | None:
        audio = self._audio_to_play
        self._audio_to_play = None
        return audio

    def get_curr_sprite(self) -> SpriteFrame:
        return self._sprite_sheet[self.state][self._frame]

    def get_curr_max_frames(self) -> int:
        return self.get_max_frames(self.state)

    def get_max_frames(self, state: str) -> int:
        return len(self._sprite_sheet[state])

    def is_looping(self) -> bool:
        return self._state_machine[self.state] == self.state
