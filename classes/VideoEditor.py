import praw, json, random, time
from classes.Subreddit import *
from moviepy.video.fx.resize import *
from classes.Data import Data
from constants import *


def rescaled_centered_clip(size, clip):
    if clip.w > clip.h:
        return resize(width=size[0], clip=clip).set_position("center")
    else:
        return resize(height=size[1], clip=clip).set_position("center")


class VideoEditor:
    def __init__(self, **kwargs):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=secret,
                                  user_agent=user_agent,
                                  username=username,
                                  password=pswd)
        self.data = Data()

    def create_video_compilation(self, **kwargs):
        preferred_duration = kwargs["preferred_duration"] if "preferred_duration" in kwargs else 600
        size = kwargs["size"] if "size" in kwargs else (1440, 900)
        subreddits, post_ratio, video_queue = {}, [], []
        index, duration = -1, 0

        def next_sub():
            nonlocal index
            index += 1
            if index == len(post_ratio):
                index = 0
            return post_ratio[index]

        for sub in kwargs["subreddits"]:
            if sub not in subreddits:
                subreddits[sub] = Subreddit(self.reddit, sub, self.data)
            post_ratio.append(subreddits[sub])

        print("making queue")
        while duration < preferred_duration:
            sub = next_sub()
            vid = sub.next_video()
            if vid:
                video_queue.append(rescaled_centered_clip(size, vid.set_start(duration)))
                duration += vid.duration
                print(f"{vid.filename[video_queue]} of {sub.subreddit.display_name} added with total duration {duration}")
                sub.set_last()
        video_queue.append(rescaled_centered_clip(size, VideoFileClip("assets/outro.mp4").set_start(duration)))

        random.shuffle(video_queue)
        final_clip = CompositeVideoClip(video_queue, size)
        print("Rendering...")
        s_time = time.time()
        final_clip.write_videofile("product/new_video.mp4")
        print(f"Render finished in {time.time() - s_time}.")