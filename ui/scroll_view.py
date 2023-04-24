from .ui_element import *


class ScrollBar(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        color: str = "#ffffff",
    ) -> None:
        super().__init__(screen, x, y, width, height)
        self.color = color


# vertical content view for ScrollView
class ContentView(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        background_color: str = "#000000",
    ) -> None:
        super().__init__(screen, x, y, width, height, background_color)
        self.__current_position = 0  # viewport current position
        self.__last_position = 0  # position of the last content element

    # move content vertically
    def move(self, step: int) -> None:
        previous_position = self.__current_position

        # update and clamp current position
        self.__current_position += step
        self.__current_position = max(0, self.__current_position)
        self.__current_position = min(
            self.__current_position, self.__last_position - self._height
        )

        # update content position
        step = previous_position - self.__current_position
        for child in self._children:
            child.y += step

    # override
    # def _update(self) -> None:
    #     self._surface.fill(self.background_color)
    #     super()._update()

    # override
    def _on_update(self) -> None:
        return

    # override
    def _on_child_added(self) -> None:
        # update the last position
        self.__last_position = max(self.__last_position, self._children[-1].y)


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
        content_background_color: str = "#000000",
    ) -> None:
        super().__init__(screen, x, y, width, height)
        self.speed = speed  # scrolling speed

        self.__content = ContentView(
            screen, 0, 0, width, height, content_background_color
        )
        self.__content.parent = self

        # self.__scroll_bar = ScrollBar()
        # self.__scroll_bar.parent = self

    # get content
    def get_content(self):
        return self.__content

    # add a UI element to the content
    def add_to_content(self, element: UIElement) -> None:
        element.parent = self.__content

    # scroll the content up or down
    def scroll(self, direction_down: bool) -> None:
        self.__content.move(-self.speed if direction_down else self.speed)

    # override
    def _on_update(self) -> None:
        return
