from pygame.surface import Surface

from src.core.collision import RectCollider
from src.core.essentials import Anchor, Pos, PosSurface, Rect
from src.core.sprite import Sprite, SpriteFrame


class Button(Sprite):
    def __init__(self, sprite_sheet: dict[str, list[SpriteFrame]], position: Pos):
        super().__init__(
            {
                "idle": "idle",
                "selected_ini": "selected",
                "selected": "selected",
                "pressed": "idle",
            },
            sprite_sheet,
            position,
            "idle",
        )
        self._just_pressed = False

    def handle_mouse_press(self, mouse_pos: Pos):
        if self.point_collision(mouse_pos):
            self.set_state("pressed")
            self._just_pressed = True

    def handle_mouse_hover(self, mouse_pos: Pos):
        hover = self.point_collision(mouse_pos)
        if not hover and self.is_looping():
            self.set_state("idle")
        if hover and self.state == "idle":
            if self._just_pressed:
                self.set_state("selected")
            else:
                self.set_state("selected_ini")
            self._just_pressed = False


class BasicButton(Button):
    def __init__(
        self,
        position: Pos,
        surfaces: dict[str, list[Surface]],
        audios: dict[tuple[str, int], str] = {},  # state, frame -> audio
        anchor: Anchor = Anchor.TOPLEFT,
    ):
        sprite_sheet = {}
        for state, sfcs in surfaces.items():
            sprite_frames = []
            for i in range(len(sfcs)):
                sfc, audio = sfcs[i], audios.get((state, i))
                rect = Rect.from_pygame(sfc.get_rect(**{anchor.name.lower(): (0, 0)}))
                pos_sfc = PosSurface(sfc, Pos(0, 0), anchor)
                sprite_frame = SpriteFrame(pos_sfc, RectCollider(rect), audio)
                sprite_frames.append(sprite_frame)
            sprite_sheet[state] = sprite_frames
        super().__init__(sprite_sheet, position)
