from .ui_element import *
from ui.text import Text
from ui.image import Image
from typing import Callable


# button
class Button(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        on_click: Callable = None,
        color_normal: str = "#ffffff",
        color_hover: str = "#DADDD8",
        color_pressed: str = "#1C1C1C",
    ) -> None:
        super().__init__(screen, x, y, width, height, color_normal)

        self.on_click = on_click

        self.color_hover = color_hover
        self.color_pressed = color_pressed

        self.__pressed = False

        self.__text = Text(self._screen, 0, 0)
        self.__text.parent = self

        image_size = min(width, height)
        self.__image = Image(self._screen, 0, 0, image_size, image_size)
        self.__image.parent = self

    # set text
    def set_text(
        self, font: pygame.font.Font, text: str = "Button", text_color: str = "#0000ff"
    ) -> None:
        self.__text.font = font
        self.__text.text = text
        self.__text.text_color = text_color

    # set image
    def set_image(self, image_path: str) -> None:
        self.__image.load_image(image_path)

    # override
    def _on_update(self) -> None:
        # check if mouse is hovering
        mouse_position = pygame.mouse.get_pos()
        if self.visible and self.get_active_area().collidepoint(mouse_position):
            # fill hover color
            self._surface.fill(self.color_hover)

            # check if left mouse is pressed
            if pygame.mouse.get_pressed()[0]:
                # fill pressed color
                self._surface.fill(self.color_pressed)

                # call onclick function if the button is not pressed yet
                if self.on_click and not self.__pressed:
                    self.__pressed = True
                    self.on_click()
            else:
                self.__pressed = False

        # draw text
        self.__text.x = self.width / 2 - self.__text.width / 2
        self.__text.y = self.height / 2 - self.__text.height / 2
