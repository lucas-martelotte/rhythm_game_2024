from pygame.surface import Surface

from src.core.collision import Collider, RectCollider
from src.core.essentials import Anchor, FPSTracker, Pos, Rect


class SpriteFrame:
    def __init__(
        self,
        surface: Surface,
        collider: Collider,
        anchor: Anchor,
        audio: str | None = None,
    ):
        self.sfc = surface  # relative_pos
        self.collider = collider  # relative_pos
        self.anchor = anchor
        self.audio = audio


class Sprite(FPSTracker):
    def __init__(
        self,
        state_machine: dict[str, str],
        sprite_sheet: dict[str, list[SpriteFrame]],
        initial_state: str,
        fps: int = 24,
    ):
        self._state_machine = state_machine
        self._sprite_sheet = sprite_sheet
        self._frame = 0
        self.state = initial_state
        self._audio_to_play: str | None = None  # handle frame loss]
        self.fps_tracker = FPSTracker(fps)

    def update(self):
        frames_passed = self.fps_tracker.get_frames_passed()
        for _ in range(frames_passed):
            self._audio_to_play = self.get_curr_sprite().audio or self._audio_to_play
            self._frame += 1
            while self._frame >= self.get_curr_max_frames():
                self._frame -= self.get_curr_max_frames()
                self.state = self._state_machine[self.state]

    def set_state(self, state: str, force_reset=False):
        if self.state != state or force_reset:
            self._frame = 0  # need to do this to trigger frame 0
        self.state = state

    def get_sfc(self) -> Surface:
        return self.get_curr_sprite().sfc

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


class BasicSprite(Sprite):
    # fmt: off
    def __init__(self, sfc: Surface, anchor: Anchor, collider_offset: Pos | None = None):
        collider_offset = collider_offset or Pos(0,0)
        rect = Rect.from_pygame(sfc.get_rect(**{anchor.name.lower(): (0,0)}))
        collider = RectCollider(rect.move(collider_offset))
        super().__init__(
            {"idle": "idle"},
            {"idle": [SpriteFrame(sfc, collider, anchor)]},
            "idle", fps = 1
        )
    # fmt: on
