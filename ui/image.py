from .ui_element import *


class Image(UIElement):
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        image_path: str = None,
    ) -> None:
        super().__init__(screen, x, y, width, height)
        self.__raw_image: pygame.Surface = None
        self.load_image(image_path)

    # load an image
    def load_image(self, image_path: str) -> None:
        if image_path:
            self.__raw_image = pygame.image.load(image_path)
            self._surface = pygame.transform.scale(self.__raw_image, self.size)
            self._surface.set_alpha(255)
        else:
            self.__raw_image = None
            self._surface.set_alpha(0)

    # override
    def _on_size_changed(self) -> None:
        if self.__raw_image:
            self._surface = pygame.transform.scale(self.__raw_image, self.size)

    # override
    def _on_update(self) -> None:
        pass
