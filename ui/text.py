from .ui_element import *


class Text(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        font: pygame.font.Font = None,
        text: str = "Text",
        text_color: str = "#ffffff",
        background_color: str = None,
    ) -> None:
        super().__init__(screen, x, y, 0, 0, background_color)
        self.__font = font
        self.__text = text
        self.__text_color = text_color

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value) -> None:
        self.__text = value
        self.__refresh_style()

    @property
    def font(self) -> pygame.font.Font:
        return self.__font

    @font.setter
    def font(self, value) -> None:
        self.__font = value
        self.__refresh_style()

    @property
    def text_color(self) -> str:
        return self.__text_color

    @text_color.setter
    def text_color(self, value: str) -> None:
        self.__text_color = value
        self.__refresh_style()

    # refresh text style
    def __refresh_style(self) -> None:
        if not self.__font:
            return

        self._surface = self.__font.render(
            self.__text, True, self.__text_color, self.background_color
        )
        self.size = self._surface.get_size()

    # override
    def _on_update(self) -> None:
        if not self.__font:
            return
        
        self._surface = self.__font.render(
            self.__text, True, self.__text_color, self.background_color
        )
