from .ui_element import *


# vertical scroll view
class ScrollView(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        speed: int = 10,
    ) -> None:
        super().__init__(screen, x, y, width, height)
        self.speed = speed
        self.__position = y  # viewport vertical position

        self._surface = pygame.Surface((self._width, self._height * 2))

    # scroll the content up or down
    def scroll(self, direction_down: bool) -> None:
        step = self.speed if direction_down else -self.speed

        for child in self._children:
            child._y += step

    def _update(self) -> None:
        self._surface.fill("#C2E7D9")
        super()._update()

    def _on_update(self) -> None:
        pass
