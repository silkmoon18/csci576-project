import time
import cv2
import pygame
import ui
from scenedetect import detect, ContentDetector

input_video_path = "data/InputVideo.mp4"
title = "csci576-project"
window_width = 960
window_height = 540
background_color = "#000000"

scene_threshold = 50
shot_threshold = 20

# test
window_width = 1500
window_height = 800


def generate_shot_buttons(index: int, scene: tuple) -> list[ui.button]:
    buttons = []
    shots = detect(
        input_video_path,
        ContentDetector(threshold=shot_threshold),
        show_progress=True,
        start_time=scene[0].get_timecode(),
        end_time=scene[1].get_timecode(),
    )
    for i, shot in enumerate(shots):
        time = to_milliseconds(shot[0].get_timecode())
        button = ui.button(
            screen,
            55 + index * 45,
            300 + i * 25,
            40,
            20,
            pygame.font.SysFont(None, 15),
            "shot_" + str(i + 1),
            lambda t=time: jump_to_time(t),
        )
        buttons.append(button)
    return buttons


def generate_scene_buttons() -> list[ui.button]:
    scenes = detect(
        input_video_path, ContentDetector(threshold=scene_threshold), show_progress=True
    )

    buttons = []
    for i, scene in enumerate(scenes):
        time = to_milliseconds(scene[0].get_timecode())
        button = ui.button(
            screen,
            10,
            300 + i * 25,
            40,
            20,
            pygame.font.SysFont(None, 15),
            "scene_" + str(i + 1),
            lambda t=time: jump_to_time(t),
        )
        buttons.append(button)
        buttons.extend(generate_shot_buttons(i, scene))

    return buttons


def to_milliseconds(time: str) -> int:
    hours, minutes, seconds = map(float, time.split(":"))
    seconds, milliseconds = map(int, str(seconds).split("."))
    return ((hours * 3600) + (minutes * 60) + seconds) * 1000 + milliseconds


def jump_to_time(ms: int) -> None:
    global capture, current_time
    capture.set(cv2.CAP_PROP_POS_MSEC, ms)
    current_time = int(capture.get(cv2.CAP_PROP_POS_FRAMES)) / 30


def test_play():
    global paused
    paused = not paused
    frame.playing = not paused


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(title)
    capture = cv2.VideoCapture(input_video_path)
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    # ui elements
    frame = ui.frame(screen, 250, 0, capture)
    play_button = ui.button(screen, 800, 30, 200, 100, font, "play", test_play)
    generate_scene_buttons()

    # main loop
    paused = True
    running = True
    current_time = 0
    duration = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) / fps)
    while running:
        screen.fill(background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                    else:
                        paused = True
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.unicode.isnumeric():
                    number = int(event.unicode)
                    if number <= len(str(duration)):
                        new_pos_sec = number * duration / 10
                        new_pos_frames = int(new_pos_sec * fps)
                        capture.set(cv2.CAP_PROP_POS_FRAMES, new_pos_frames)
                        current_time = new_pos_sec
                        paused = True

        if not paused:
            current_time += 1 / fps

        text_surface = font.render(
            "{:.2f} / {:.2f}".format(current_time, duration), True, (255, 255, 255)
        )
        screen.blit(text_surface, (10, 10))

        ui.ui_element.update_all()
        pygame.display.update()

        clock.tick(fps)

    # clean up
    capture.release()
    pygame.quit()
    quit()
