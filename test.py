from moviepy.editor import *


clip1 = VideoFileClip("source/WinStupidPrices/2/lcm3jo.mp4")
clip2 = VideoFileClip("source/WinStupidPrices/2/lf8znv.mp4").set_start(clip1.duration)

f_video = CompositeVideoClip([clip1, clip2])
f_video.write_videofile("test.mp4")