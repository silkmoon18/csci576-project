from video_player import VideoPlayer

title = "csci576-project"
background_color = "#282C34"

# adaptive threshold
scene_threshold = 8
shot_threshold = 6
subshot_threshold = 4

window_width = 1500
window_height = 800

if __name__ == "__main__":
    player = VideoPlayer(
        title,
        window_width,
        window_height,
        scene_threshold,
        shot_threshold,
        subshot_threshold,
        background_color,
    )
    player.start()
