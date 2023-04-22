import cv2
import pygame
import ui
from scenedetect import detect, AdaptiveDetector, FrameTimecode


class VideoPlayer:
    def __init__(
        self,
        input_video_path: str,
        title: str,
        window_width: int,
        window_height: int,
        background_color: str = "#000000",
        scene_threshold: float = 40,
        shot_threshold: float = 27,
    ):
        self.__video_path = input_video_path
        self.title = title
        self.window_width = window_width
        self.window_height = window_height
        self.background_color = background_color
        self.__scene_threshold = scene_threshold
        self.__shot_threshold = shot_threshold

        self.__running = True

        self.__init_pygame()
        self.__init_interface()

        self.__process_video()

    # start the player
    def start(self):
        while self.__running:
            self.__handle_events()
            self.__update()

        pygame.quit()
        quit()

    # initialize pygame and related properties
    def __init_pygame(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.__screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    # initialize UI interface
    def __init_interface(self):
        self.__video_frame = ui.VideoFrame(self.__screen, 250, 0, self.__video_path)
        self.__play_button = ui.Button(
            self.__screen, 800, 30, 200, 100, self.font, "play", self.__video_frame.play
        )
        self.__pause_button = ui.Button(
            self.__screen,
            1025,
            30,
            200,
            100,
            self.font,
            "pause",
            self.__video_frame.pause,
        )
        self.__stop_button = ui.Button(
            self.__screen,
            1250,
            30,
            200,
            100,
            self.font,
            "stop",
            self.__video_frame.stop,
        )

    # handle the player events
    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__paused = not self.__paused
                elif event.key == pygame.K_ESCAPE:
                    self.__running = False

    def __update(self):
        self.__screen.fill(self.background_color)

        text_surface = self.font.render(
            "{:.2f} / {:.2f}".format(
                self.__video_frame.current_time, self.__video_frame.duration
            ),
            True,
            (255, 255, 255),
        )
        self.__screen.blit(text_surface, (10, 10))

        ui.UIElement.update_all()
        pygame.display.update()

        self.clock.tick(self.__video_frame.fps)

    # process current video
    # TODO: better interactivity
    def __process_video(self):
        scenes = detect(
            self.__video_path,
            AdaptiveDetector(adaptive_threshold=self.__scene_threshold),
            show_progress=True,
        )
        self.__make_scene_buttons(scenes)

    # make index buttons for scenes
    # TODO: better interactivity
    def __make_scene_buttons(
        self, scenes: list[tuple[FrameTimecode, FrameTimecode]]
    ) -> list[ui.Button]:
        buttons = []
        for i, scene in enumerate(scenes):
            time = scene[0].get_seconds()
            button = ui.Button(
                self.__screen,
                10,
                300 + i * 25,
                40,
                20,
                pygame.font.SysFont(None, 15),
                "scene_" + str(i + 1),
                lambda t=time: self.__video_frame.jump_to(t),
            )
            buttons.append(button)
            buttons.extend(self.__make_shot_buttons(i, scene))

        return buttons

    # make index buttons for shots
    # TODO: better interactivity
    def __make_shot_buttons(
        self, index: int, scene: tuple[FrameTimecode, FrameTimecode]
    ) -> list[ui.Button]:
        buttons = []
        shots = detect(
            self.__video_path,
            AdaptiveDetector(adaptive_threshold=self.__shot_threshold),
            show_progress=True,
            start_time=scene[0].get_timecode(),
            end_time=scene[1].get_timecode(),
        )
        for i, shot in enumerate(shots):
            time = shot[0].get_seconds()
            button = ui.Button(
                self.__screen,
                55 + index * 45,
                300 + i * 25,
                40,
                20,
                pygame.font.SysFont(None, 15),
                "shot_" + str(i + 1),
                lambda t=time: self.__video_frame.jump_to(t),
            )
            buttons.append(button)
        return buttons
