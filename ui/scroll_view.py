from .ui_element import *


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
            self.__current_position, self.__last_position - self.height
        )

        # update content position
        step = previous_position - self.__current_position
        for child in self._children:
            child.y += step

    # get current progress
    def get_progress(self) -> float:
        if self.__last_position == 0:
            return 0
        return self.__current_position / self.__last_position

    # get the length of content
    def get_length(self) -> int:
        return self.__last_position
    
    # clear all content elements
    def clear(self)->None:
        self.delete_all_children()
        self.__current_position = 0
        self.__last_position = 0

    # override
    def _on_update(self) -> None:
        return

    # override
    def _on_child_added(self) -> None:
        child = self._children[-1]
        # update the last position
        self.__last_position = max(self.__last_position, child.y + child.height)


# scroll bar for ScrollView
class ScrollBar(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        scroll_view_width: int,
        scroll_view_height: int,
        width: int = 10,
        color_normal: str = "#ffffff",
        color_hover: str = "#DADDD8",
        color_pressed: str = "#1C1C1C",
    ) -> None:
        super().__init__(
            screen,
            scroll_view_width - width,
            0,
            width,
            scroll_view_height,
            color_normal,
        )
        self.color_hover = color_hover
        self.color_dragging = color_pressed

        self.__dragging = False

    @property
    def dragging(self)->bool:
        return self.__dragging

    # override
    def _on_update(self) -> None:
        mouse_position = pygame.mouse.get_pos()

        # if the bar is being dragged
        if self.__dragging and pygame.mouse.get_pressed()[0]:
            # fill dragging color
            self._surface.fill(self.color_dragging)
            return

        self.__dragging = False
        # check if mouse is hovering
        if self.visible and self.get_active_area().collidepoint(mouse_position):
            # fill hover color
            self._surface.fill(self.color_hover)

            # check if left mouse is pressed
            if pygame.mouse.get_pressed()[0]:
                # fill pressed color
                self._surface.fill(self.color_dragging)

                # start dragging
                self.__dragging = True


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

        self.__scroll_bar = ScrollBar(screen, width, height)
        self.__scroll_bar.parent = self
        self.__previous_mouse_position = 0 # for calculating mouse delta position

    # add a UI element to the content
    def add_to_content(self, element: UIElement) -> None:
        element.parent = self.__content

        # update bar size
        self.__scroll_bar.height = (
            self.height / self.__content.get_length() * self.height
        )

    # clear content
    def clear_content(self) -> None:
        self.__content.clear()
        self.__scroll_bar.y = 0
        self.__scroll_bar.height = self.height

    # scroll the content up or down
    def scroll(self, direction_down: bool) -> None:
        # scroll only when mouse is on the area
        mouse_position = pygame.mouse.get_pos()
        if not self.visible or not self.get_active_area().collidepoint(mouse_position):
            return

        step = -self.speed if direction_down else self.speed
        self.__content.move(step)

        # update bar position
        self.__scroll_bar.y = self.__content.get_progress() * self.height

    # override
    def _on_update(self) -> None:
        mouse_position = pygame.mouse.get_pos()

        # if is dragging scroll bar, move content
        if self.__scroll_bar.dragging:
            step = (
                (mouse_position[1] - self.__previous_mouse_position)
                * self.__content.get_length()
                / self.height
            )
            self.__content.move(step)
            self.__scroll_bar.y = self.__content.get_progress() * self.height

        self.__previous_mouse_position = mouse_position[1]
