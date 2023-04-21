from scenedetect import detect, ContentDetector, split_video_ffmpeg

inputVideoPath = 'data/InputVideo.mp4'
threshold = 20

scene_list = detect(inputVideoPath, ContentDetector(threshold=threshold), show_progress=True)
for i, scene in enumerate(scene_list):
    print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
        i+1,
        scene[0].get_timecode(), scene[0].get_frames(),
        scene[1].get_timecode(), scene[1].get_frames(),))