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
        self.__content_elements: list[UIElement] = []

        self._surface = pygame.Surface((self._width, self._height * 2))

        # debug

        # font = pygame.font.SysFont(None, 24)
        # text = font.render("This is a scrollable view window", True, (0, 0, 0))
        # text_rect = text.get_rect(center=(self._width // 2, self._height // 2))

        # self._surface.blit(text, text_rect)

    def scroll(self, direction_down: bool):
        step = self.speed if direction_down else -self.speed
        # self._surface.scroll(0, step)

        for element in self.__content_elements:
            element._y += step

    def add(self, element: UIElement):
        self.__content_elements.append(element)
        element.parent = self
        # self._surface.blit(element._surface, element._rect)

    def _update(self) -> None:
        self._surface.fill("#C2E7D9")
        super()._update()

    def _on_update(self) -> None:
        pass
