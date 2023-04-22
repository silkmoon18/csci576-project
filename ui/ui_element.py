from __future__ import annotations
from abc import ABC, abstractmethod
import pygame


# abstract class for ui elements
class UIElement(ABC):
    elements: list[UIElement] = []  # list of all ui elements

    # update all elements
    @staticmethod
    def update_all() -> None:
        for element in UIElement.elements:
            if element._parent:
                continue
            element.__update()

    # initialize an element with a target surface, position, and dimension
    def __init__(
        self, screen: pygame.Surface, x: int, y: int, width: int, height: int
    ) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self._surface = pygame.Surface((self.width, self.height))
        self._rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self._children: list[UIElement] = []
        self._parent = None

        self.visible = True
        UIElement.elements.append(self)

    @property
    def parent(self) -> UIElement:
        return self._parent

    @parent.setter
    def parent(self, value: UIElement) -> None:
        # if parent exists, remove it
        if self._parent:
            self._parent._children.remove(self)

        # set the new parent and add this to its child list
        self._parent = value
        if value:
            value._children.append(self)

    # update the element and its children once per frame
    def __update(self) -> None:
        self._on_update()
        self.__draw()
        for child in self._children:
            child._on_update()
            child.__draw()

    # draw the element to the screen
    def __draw(self) -> None:
        if not self.visible:
            return
        self.screen.blit(self._surface, self._rect)

    # called on update
    @abstractmethod
    def _on_update(self) -> None:
        pass
