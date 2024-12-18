from pygame.surface import Surface

from src.core.collision import RectCollider
from src.core.entity import RenderableEntity, Sprite, SpriteFrame
from src.core.essentials import Anchor, Pos, Rect


class Button(RenderableEntity):
    def __init__(self, sprite_sheet: dict[str, list[SpriteFrame]], position: Pos):
        sprite = Sprite(
            {
                "idle": "idle",
                "selected_ini": "selected",
                "selected": "selected",
                "pressed": "idle",
            },
            sprite_sheet,
            "idle",
            fps=30,
        )
        super().__init__(sprite, position)
        self._just_pressed = False

    def handle_mouse_press(self, mouse_pos: Pos):
        if self.point_collision(mouse_pos):
            self.sprite.set_state("pressed")
            self._just_pressed = True

    def handle_mouse_hover(self, mouse_pos: Pos):
        hover, sprite = self.point_collision(mouse_pos), self.sprite
        if not hover and sprite.is_looping():
            self._just_pressed = False
            sprite.set_state("idle")
        if hover and sprite.state == "idle":
            if self._just_pressed:
                sprite.set_state("selected")
            else:
                sprite.set_state("selected_ini")


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
                sprite_frame = SpriteFrame(sfc, RectCollider(rect), anchor, audio)
                sprite_frames.append(sprite_frame)
            sprite_sheet[state] = sprite_frames
        super().__init__(sprite_sheet, position)
