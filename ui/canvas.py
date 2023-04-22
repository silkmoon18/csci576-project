from .ui_element import *


# TODO
class Canvas(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        color: str = "#000000",
    ) -> None:
        super().__init__(screen, x, y, width, height)
        self.color = color

    def _on_update(self) -> None:
        self.screen.fill(self.color)
