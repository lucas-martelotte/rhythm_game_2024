from pygame.font import Font, SysFont
from pygame.surface import Surface

from src.core.utils import get_text_list_surface, wrap_text


class Textbox:
    def __init__(
        self,
        size: tuple[int, int],
        font: Font = SysFont("comicsans", 24),
        text_color: tuple[int, int, int] = (0, 0, 0),
        text: str = "",
        textbox_color: tuple[int, int, int] = (255, 255, 255),
        alpha: int = 0,
        padding: tuple[int, int] = (0, 0),  # resp. horizontal, vertical
    ):
        self.width, self.height = size
        self.font = font
        self.text = text
        self.text_color = text_color
        self.padding = padding
        self.rgba = (textbox_color[0], textbox_color[1], textbox_color[2], alpha)

    def get_sfc(self) -> Surface:
        lines = wrap_text(self.text, self.font, self.width - 2 * self.padding[0])
        text_sfc = get_text_list_surface(lines, self.font, self.text_color)
        output_sfc = Surface((self.width, self.height)).convert_alpha()
        output_sfc.fill(self.rgba)
        output_sfc.blit(text_sfc, self.padding)
        return output_sfc
