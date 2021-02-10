from classes.VideoEditor import *
from moviepy.editor import *

video_editor = VideoEditor()
print("Editor is ready")
video_editor.create_video_compilation(preferred_duration=30, subreddits=["WinStupidPrizes", "brr"])
