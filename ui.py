from abc import ABC, abstractmethod
import pygame
import cv2
from typing import Callable


# abstract class for ui elements
class ui_element(ABC):
    elements = []

    @staticmethod
    def update_all() -> None:
        for element in ui_element.elements:
            if element.parent:
                continue
            element.update()

    def __init__(
        self, screen: pygame.Surface, x: int, y: int, width: int, height: int
    ) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.visible = True
        self.children = []
        self.parent = None
        ui_element.elements.append(self)

    def setParent(self, parent: "ui_element") -> None:
        if parent:
            parent.children.append(self)
            self.parent = parent
        else:
            self.parent.children.remove(self)
            self.parent = None

    def update(self) -> None:
        self.on_update()
        self.draw()
        for child in self.children:
            child.on_update()
            child.draw()

    def draw(self) -> None:
        if not self.visible:
            return
        self.screen.blit(self.surface, self.rect)

    @abstractmethod
    def on_update(self) -> None:
        pass


# button
class button(ui_element):
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

    def on_update(self) -> None:
        self.surface.fill(self.color_normal)

        mousePos = pygame.mouse.get_pos()
        if self.visible and self.rect.collidepoint(mousePos):
            self.surface.fill(self.color_hover)

            if pygame.mouse.get_pressed()[0]:
                self.surface.fill(self.color_pressed)

                if self.on_click and not self.pressed:
                    self.pressed = True
                    self.on_click()
            else:
                self.pressed = False


        self.surface.blit(
            self.text,
            [
                self.rect.width / 2 - self.text.get_rect().width / 2,
                self.rect.height / 2 - self.text.get_rect().height / 2,
            ],
        )


# frame for video
class frame(ui_element):
    def __init__(
        self, screen: pygame.Surface, x: int, y: int, capture: "cv2.VideoCapture"
    ) -> None:
        super().__init__(
            screen,
            x,
            y,
            int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
        self.capture = capture
        self.frame = capture.read()[1]
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
        self.playing = False

    def on_update(self) -> None:
        if self.playing:
            ret, self.frame = self.capture.read()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
            if not ret:
                self.playing = False

        self.surface = pygame.surfarray.make_surface(self.frame)


# class text_input(ui_element):
#     def __init__(self, screen: pygame.Surface, x: int, y: int, width: int, height: int) -> None:


# canvas
class canvas(ui_element):
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

    def on_update(self) -> None:
        self.screen.fill(self.color)
