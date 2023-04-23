from video_player import VideoPlayer

title = "csci576-project"
window_width = 960
window_height = 540
background_color = "#000000"

# content threshold
# scene_threshold = 40
# shot_threshold = 27

# adaptive threshold
scene_threshold = 8
shot_threshold = 6

# test
window_width = 1500
window_height = 800


if __name__ == "__main__":
    player = VideoPlayer(
        title,
        window_width,
        window_height,
        background_color,
        scene_threshold,
        shot_threshold,
    )
    player.start()
