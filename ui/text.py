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
        self.__font = font
        self.__text = text
        self.text_color = text_color
        self.background_color = background_color

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        self.__refresh_style()

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, value):
        self.__font = value
        self.__refresh_style()

    def __refresh_style(self) -> None:
        self._surface = self.font.render(
            self.__text, True, self.text_color, self.background_color
        )
        self._width, self._height = self._surface.get_size()
        self._rect = pygame.Rect(0, 0, self._width, self._height)

    def _on_update(self) -> None:
        return
