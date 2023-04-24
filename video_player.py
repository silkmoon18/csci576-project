import pygame
import ui
from tkinter import Tk, filedialog
from scenedetect import detect, AdaptiveDetector, FrameTimecode


class VideoPlayer:
    def __init__(
        self,
        title: str,
        window_width: int,
        window_height: int,
        scene_threshold: float,
        shot_threshold: float,
        background_color: str = "#000000",
        program_fps: int = 60,
    ):
        self.title = title
        self.window_width = window_width
        self.window_height = window_height
        self.background_color = background_color
        self.__scene_threshold = scene_threshold
        self.__shot_threshold = shot_threshold
        self.__program_fps = program_fps

        self.__running = True

        # NOTE: tkinter has to be initialized before pygame, else pygame will crash on macOS
        self.__init_tkinter()
        self.__init_pygame()
        self.__init_interface()

    # start the player
    def start(self):
        while self.__running:
            self.__handle_events()
            self.__update()

        pygame.quit()
        quit()

    # initialize tkinter root
    def __init_tkinter(self):
        self.__tk = Tk()
        self.__tk.withdraw()  # hide root window

    # initialize pygame and related properties
    def __init_pygame(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.__screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.__clock = pygame.time.Clock()
        self.__font = pygame.font.SysFont(None, 24)

    # initialize UI interface
    def __init_interface(self):
        # init ui elements
        self.__video_frame = ui.VideoFrame(self.__screen, 250, 0)
        self.__progress_text = ui.Text(self.__screen, 10, 10, self.__font)

        self.__buttons_scroll_view = ui.ScrollView(
            self.__screen, 10, 300, 400, 400, content_background_color="#C2E7D9"
        )

        self.__open_button = ui.Button(
            self.__screen, 800, 150, 200, 100, self.__font, "open", self.__open_video
        )
        self.__play_button = ui.Button(
            self.__screen,
            800,
            30,
            200,
            100,
            self.__font,
            "play",
            self.__video_frame.play,
        )
        self.__pause_button = ui.Button(
            self.__screen,
            1025,
            30,
            200,
            100,
            self.__font,
            "pause",
            self.__video_frame.pause,
        )
        self.__stop_button = ui.Button(
            self.__screen,
            1250,
            30,
            200,
            100,
            self.__font,
            "stop",
            self.__video_frame.stop,
        )

    # handle the player events
    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            # keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__video_frame.toggle()
                elif event.key == pygame.K_ESCAPE:
                    self.__running = False

            # mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # scroll up
                if event.button == 4:
                    # move content down
                    self.__buttons_scroll_view.scroll(True)
                # scroll down
                elif event.button == 5:
                    # move content up
                    self.__buttons_scroll_view.scroll(False)

    # do updates
    def __update(self):
        self.__screen.fill(self.background_color)

        self.__progress_text.text = "{:.2f} / {:.2f}".format(
            self.__video_frame.current_time, self.__video_frame.duration
        )

        ui.UIElement.update_all()
        pygame.display.update()

        self.__clock.tick(self.__program_fps)

    # open a video
    def __open_video(self):
        self.__video_path = filedialog.askopenfilename(
            initialdir=".",
            title="Select a mp4 file",
            filetypes=(("MP4 files", "*.mp4"),),
        )
        if not self.__video_path:
            return

        self.__buttons_scroll_view.clear_content()
        self.__video_frame.load_video(self.__video_path)
        self.__video_frame.set_interval(self.__program_fps)
        self.__process_video()

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
        font_size: int = 15
        width: int = 40
        height: int = 20
        margin_x: int = 5
        margin_y: int = 5

        scene_buttons = []

        y = margin_y
        for i, scene in enumerate(scenes):
            time = scene[0].get_seconds()
            scene_button = ui.Button(
                self.__screen,
                margin_x,
                y,
                width,
                height,
                pygame.font.SysFont(None, font_size),
                "scene_" + str(i + 1),
                lambda t=time: self.__video_frame.jump_to(t),
            )
            self.__buttons_scroll_view.add_to_content(scene_button)
            scene_buttons.append(scene_button)

            shot_buttons = self.__make_shot_buttons(scene_button, scene)
            if len(shot_buttons) > 0:
                last = shot_buttons[-1]
                y = last.y + last.height
            else:
                y = scene_button.y + height
            y += margin_y

            scene_buttons.extend(shot_buttons)

        return scene_buttons

    # make index buttons for shots
    # TODO: better interactivity
    def __make_shot_buttons(
        self,
        scene_button: ui.Button,
        scene: tuple[FrameTimecode, FrameTimecode],
        font_size: int = 15,
        width: int = 40,
        height: int = 20,
        margin_x: int = 5,
        margin_y: int = 5,
    ) -> list[ui.Button]:
        buttons = []
        shots = detect(
            self.__video_path,
            AdaptiveDetector(adaptive_threshold=self.__shot_threshold),
            show_progress=True,
            start_time=scene[0].get_timecode(),
            end_time=scene[1].get_timecode(),
        )

        start_position = (
            scene_button.x + scene_button.width + margin_x,
            scene_button.y + scene_button.height + margin_y,
        )
        for i, shot in enumerate(shots):
            time = shot[0].get_seconds()
            button = ui.Button(
                self.__screen,
                start_position[0],
                start_position[1] + i * (height + margin_y),
                width,
                height,
                pygame.font.SysFont(None, font_size),
                "shot_" + str(i + 1),
                lambda t=time: self.__video_frame.jump_to(t),
            )
            self.__buttons_scroll_view.add_to_content(button)
            buttons.append(button)
        return buttons
