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
        font: pygame.font,
        button_text: str = "Button",
        on_click: Callable = None,
        color_normal: str = "#ffffff",
        color_hover: str = "#DADDD8",
        color_pressed: str = "#1C1C1C",
    ) -> None:
        super().__init__(screen, x, y, width, height)

        self.on_click = on_click

        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_pressed = color_pressed

        self.text = font.render(button_text, True, (20, 20, 20))

        self.pressed = False

    def _on_update(self) -> None:
        # fill normal color
        self._surface.fill(self.color_normal)

        # check if mouse is hovering
        mousePos = pygame.mouse.get_pos()
        if self.visible and self._rect.collidepoint(mousePos):
            # fill hover color
            self._surface.fill(self.color_hover)

            # check if left mouse is pressed
            if pygame.mouse.get_pressed()[0]:
                # fill pressed color
                self._surface.fill(self.color_pressed)

                # call onclick function if the button is not pressed yet
                if self.on_click and not self.pressed:
                    self.pressed = True
                    self.on_click()
            else:
                self.pressed = False

        # draw text
        self._surface.blit(
            self.text,
            [
                self._rect.width / 2 - self.text.get_rect().width / 2,
                self._rect.height / 2 - self.text.get_rect().height / 2,
            ],
        )