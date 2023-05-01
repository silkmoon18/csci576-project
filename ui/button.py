from .ui_element import *
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
        font: pygame.font.Font,
        button_text: str = "Button",
        on_click: Callable = None,
        color_normal: str = "#ffffff",
        color_hover: str = "#DADDD8",
        color_pressed: str = "#1C1C1C",
    ) -> None:
        super().__init__(screen, x, y, width, height, color_normal)

        self.on_click = on_click

        self.color_hover = color_hover
        self.color_pressed = color_pressed

        self.text = font.render(button_text, True, "#ffffff")

        self.__pressed = False

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
        self._surface.blit(
            self.text,
            [
                self.width / 2 - self.text.get_rect().width / 2,
                self.height / 2 - self.text.get_rect().height / 2,
            ],
        )
