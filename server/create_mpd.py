from ffmpeg_streaming import input, Formats
from pathlib import Path

# BigBuckBunny video url
# https://www.youtube.com/watch?v=aqz-KE-bpKQ
# or
# https://s3.us-west-1.wasabisys.com/public-assets/original.mkv
video_path = "original.mkv"
video = input(video_path)
dash = video.dash(Formats.vp9())
dash.auto_generate_representations()
Path("result").mkdir(exist_ok=True)
dash.output('./result/dash.mpd')
