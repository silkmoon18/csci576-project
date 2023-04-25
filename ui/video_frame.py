from .ui_element import *
import cv2


# frame that displays a video
class VideoFrame(UIElement):
    def __init__(
        self, screen: pygame.Surface, x: int, y: int, width: int, height: int
    ) -> None:
        super().__init__(screen, x, y, width, height)

        self.__frame = None
        self.__capture: cv2.VideoCapture = None
        self.__raw_width, self.__raw_height = 0, 0
        self.__fps = 0
        self.__duration = 0
        self.__current_time = 0

        self.__update_interval = 0
        self.__frame_count = 0
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

    # toggle playing state
    def toggle(self) -> None:
        self.__playing = not self.__playing

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

    # set the update interval based on program fps
    def set_interval(self, program_fps: int) -> None:
        if not self.__capture:
            return

        video_fps = int(self.__capture.get(cv2.CAP_PROP_FPS))
        self.__update_interval = max(1, program_fps / video_fps)
        self.__frame_count = 0

    # load a video from the specified path
    def load_video(self, video_path: str = None) -> None:
        if self.__capture:
            self.__capture.release()

        if video_path:
            self.__capture = cv2.VideoCapture(video_path)
            self.__fps = int(self.__capture.get(cv2.CAP_PROP_FPS))
            self.__raw_width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.__raw_height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.__duration = int(
                self.__capture.get(cv2.CAP_PROP_FRAME_COUNT) / self.__fps
            )
        else:
            self.__capture = None
            self.__fps = 0
            self.__raw_width = 0
            self.__raw_height = 0
            self.__duration = 0

        self.__current_time = 0
        self.__next()

    # jump to the specified time in seconds
    def jump_to(self, time: float) -> None:
        self.__capture.set(cv2.CAP_PROP_POS_MSEC, time * 1000)
        self.__current_time = (
            int(self.__capture.get(cv2.CAP_PROP_POS_FRAMES)) / self.__fps
        )
        self.__next()

    # override
    def _on_update(self) -> None:
        # if video is playing
        if self.__playing:
            # increment counter
            self.__frame_count += 1

            # if counter reached the interval to update
            if self.__frame_count >= self.__update_interval:
                self.__frame_count = 0

                # try update video frame
                updated = self.__next()
                self.__current_time += 1 / self.__fps
                self.__current_time = max(0, min(self.__duration, self.__current_time))
                if not updated:
                    self.__playing = False

        # always display a frame
        if self.__frame is not None:
            self._surface = pygame.surfarray.make_surface(self.__frame)

    # move to the next frame
    def __next(self) -> bool:
        if not self.__capture:
            return False

        success, self.__frame = self.__capture.read()
        if not success:
            return False

        self.__frame = cv2.resize(self.__frame, (self.width, self.height))
        self.__frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
        return True
