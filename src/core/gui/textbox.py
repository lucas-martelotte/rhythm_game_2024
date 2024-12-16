from pygame.font import Font, SysFont
from pygame.surface import Surface

from src.core.utils import get_text_list_surface, wrap_text


class Textbox:
    def __init__(
        self,
        size: tuple[int, int],
        font: Font = SysFont("comicsans", 24),
        colour: tuple[int, int, int] = (0, 0, 0),
        text: str = "",
        color: tuple[int, int, int] = (255, 255, 255),
        alpha: int = 0,
    ):
        self.width, self.height = size
        self.font = font
        self.text = text
        self.colour = colour
        self.rgba = (color[0], color[1], color[2], alpha)

    def get_sfc(self) -> Surface:
        lines = wrap_text(self.text, self.font, self.width)
        text_sfc = get_text_list_surface(lines, self.font, self.colour)
        output_sfc = Surface((self.width, self.height)).convert_alpha()
        output_sfc.fill(self.rgba)
        output_sfc.blit(text_sfc, (0, 0))
        return output_sfc
