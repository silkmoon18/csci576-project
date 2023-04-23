from .ui_element import *
import cv2


# frame that displays a video
class VideoFrame(UIElement):
    def __init__(
        self, screen: pygame.Surface, x: int, y: int, video_path: str = None
    ) -> None:
        self.__capture: cv2.VideoCapture = None
        self.load_video(video_path)
        super().__init__(screen, x, y, self.width, self.height)
        self.__next()
        self.__playing = False

    @property
    def fps(self) -> int:
        return self.__fps

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def current_time(self) -> int:
        return self.__current_time

    # play the video
    def play(self) -> None:
        self.__playing = True

    # pause the video
    def pause(self) -> None:
        self.__playing = False

    # move to the beginning and pause the video
    def stop(self) -> None:
        self.__playing = False
        self.jump_to(0)

    # load a video from the specified path
    def load_video(self, video_path: str = None) -> None:
        if self.__capture:
            self.__capture.release()
        self.__capture = cv2.VideoCapture(video_path)
        self.__fps = int(self.__capture.get(cv2.CAP_PROP_FPS))
        self.width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.__current_time = 0
        if self.__fps > 0:
            self.__duration = int(
                self.__capture.get(cv2.CAP_PROP_FRAME_COUNT) / self.__fps
            )
        else:
            self.__duration = 0

    # jump to the specified time in seconds
    def jump_to(self, time: float) -> None:
        self.__capture.set(cv2.CAP_PROP_POS_MSEC, time * 1000)
        self.__current_time = (
            int(self.__capture.get(cv2.CAP_PROP_POS_FRAMES)) / self.__fps
        )
        self.__next()

    def _on_update(self) -> None:
        if self.__playing:
            updated = self.__next()
            self.__current_time += 1 / self.__fps
            if not updated:
                self.__playing = False

        if self.__frame is not None:
            self._surface = pygame.surfarray.make_surface(self.__frame)

    # move to the next frame
    def __next(self) -> bool:
        success, self.__frame = self.__capture.read()
        if not success:
            return False

        self.__frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
        return True