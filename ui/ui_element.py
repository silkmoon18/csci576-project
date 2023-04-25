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
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        background_color: str = None,
    ) -> None:
        self._screen = screen
        self.x = x
        self.y = y
        self.__width = width
        self.__height = height
        self.background_color = background_color

        self._surface = pygame.Surface((self.__width, self.__height))
        self._rect = pygame.Rect(0, 0, self.__width, self.__height)
        self._children: list[UIElement] = []
        self._parent = None

        self.visible = True
        UIElement.elements.append(self)

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, value: int) -> None:
        self.__width = value
        self.__refresh_size()

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, value: int) -> None:
        self.__height = value
        self.__refresh_size()

    @property
    def size(self) -> tuple[int, int]:
        return (self.__width, self.__height)

    @size.setter
    def size(self, value: tuple[int, int]) -> None:
        self.__width = value[0]
        self.__height = value[1]
        self.__refresh_size()

    # get the rect in world space
    @property
    def world_rect(self) -> pygame.Rect:
        x, y = self.x, self.y
        if self._parent:
            parent_rect = self._parent.world_rect
            x += parent_rect.x
            y += parent_rect.y
        return pygame.Rect(x, y, self.__width, self.__height)

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

    # delete this element and all its children
    def delete(self) -> None:
        self.delete_all_children()
        self.background_color = None
        self._surface = None
        self._rect = None
        self.parent = None
        self.visible = False
        UIElement.elements.remove(self)

    # delete all children
    def delete_all_children(self) -> None:
        while self._children:
            self._children[-1].delete()

    # update the element and its children once per frame
    def __update(self) -> None:
        # if background color is not None, fill the surface
        if self.background_color:
            self._surface.fill(self.background_color)

        self._on_update()
        for child in self._children:
            child.__update()
        self.__draw()

    # draw the element to the screen
    def __draw(self) -> None:
        if not self.visible:
            return

        # draw on the screen
        surface = self._screen

        # if parent exists, draw on the parent's surface
        if self._parent:
            surface = self._parent._surface
        surface.blit(self._surface, (self.x, self.y), self._rect)

    # refresh the sizes of surface and rect
    def __refresh_size(self) -> None:
        self._surface = pygame.Surface((self.__width, self.__height))
        self._rect = pygame.Rect(
            self._rect.x, self._rect.y, self.__width, self.__height
        )
        self._on_size_changed()

    # called on update
    @abstractmethod
    def _on_update(self) -> None:
        pass

    # called when a new child is added
    def _on_child_added(self) -> None:
        pass

    # called when the size is changed
    def _on_size_changed(self) -> None:
        pass