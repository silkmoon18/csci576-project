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
        super().__init__(screen, x, y, 80, 20, background_color)
        self.__font = font
        self.__text = text
        self.text_color = text_color

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value) -> None:
        self.__text = value
        self.__refresh_style()

    @property
    def font(self) -> pygame.font:
        return self.__font

    @font.setter
    def font(self, value) -> None:
        self.__font = value
        self.__refresh_style()

    # refresh text style
    def __refresh_style(self) -> None:
        self._surface = self.font.render(
            self.__text, True, self.text_color, self.background_color
        )
        self._width, self._height = self._surface.get_size()
        self._rect = pygame.Rect(0, 0, self._width, self._height)

    # override
    def _on_update(self) -> None:
        return
