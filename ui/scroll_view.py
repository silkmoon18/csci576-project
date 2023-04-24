from .ui_element import *


# vertical scroll view
class ScrollView(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,  # aq
        x: int,
        y: int,
        width: int,
        height: int,
        speed: int = 10,
        background_color: str = "#000000",
    ) -> None:
        super().__init__(screen, x, y, width, height)
        self.speed = speed  # scrolling speed
        self.background_color = background_color

        self.__current_position = 0  # viewport current position
        self.__last_position = 0  # position of the last content element

    # scroll the content up or down
    def scroll(self, direction_down: bool) -> None:
        previous_position = self.__current_position

        # update and clamp current position
        self.__current_position += -self.speed if direction_down else self.speed
        self.__current_position = max(0, self.__current_position)
        self.__current_position = min(
            self.__current_position, self.__last_position - self._height
        )

        # update content position
        step = previous_position - self.__current_position
        for child in self._children:
            child.y += step

    # override
    def _update(self) -> None:
        self._surface.fill(self.background_color)
        super()._update()

    # override
    def _on_update(self) -> None:
        pass

    # override
    def _on_child_added(self) -> None:
        # update the last position
        self.__last_position = max(self.__last_position, self._children[-1].y)
