from .ui_element import *


class Text(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        font: pygame.font,
        text: str = "Text",
        text_color: str = "#ffffff",
        background_color: str = None,
    ) -> None:
        super().__init__(screen, x, y, 0, 0)
        self.font = font
        self.text = text
        self.text_color = text_color
        self.background_color = background_color

    def _on_update(self) -> None:
        self._surface = self.font.render(
            self.text, True, self.text_color, self.background_color
        )
