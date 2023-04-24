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
            element._update()

    # initialize an element with a target surface, position, and dimension
    def __init__(
        self, screen: pygame.Surface, x: int, y: int, width: int, height: int
    ) -> None:
        self._screen = screen
        self.x = x
        self.y = y
        self._width = width
        self._height = height

        self._surface = pygame.Surface((self._width, self._height))
        self._rect = pygame.Rect(0, 0, self._width, self._height)
        self._children: list[UIElement] = []
        self._parent = None

        self.visible = True
        UIElement.elements.append(self)

    @property
    def size(self) -> tuple[int, int]:
        return (self._width, self._height)

    # get the rect in world space
    @property
    def world_rect(self) -> pygame.Rect:
        x, y = self.x, self.y
        if self._parent:
            parent_rect = self._parent.world_rect
            x += parent_rect.x
            y += parent_rect.y
        return pygame.Rect(x, y, self._width, self._height)

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
            value._on_child_added()

    # get the active area in world space
    def get_active_area(self) -> pygame.Rect:
        area = self.world_rect
        if self._parent:
            area = area.clip(self._parent.get_active_area())
        return area

    # update the element and its children once per frame
    def _update(self) -> None:
        self._on_update()
        for child in self._children:
            child._on_update()
            child._draw()
        self._draw()

    # draw the element to the screen
    def _draw(self) -> None:
        if not self.visible:
            return

        surface = self._screen
        if self._parent:
            surface = self._parent._surface
        surface.blit(self._surface, (self.x, self.y), self._rect)

    # called on update
    @abstractmethod
    def _on_update(self) -> None:
        pass

    # called when a new child is added
    def _on_child_added(self) -> None:
        pass
