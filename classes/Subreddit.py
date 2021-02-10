from moviepy.editor import *


class Subreddit:
    def __init__(self, reddit, sub, data):
        self.subreddit = reddit.subreddit(sub)
        self.data = data
        if self.subreddit.display_name not in self.data.data["subreddits"]:
            self.data.data["subreddits"][self.subreddit.display_name] = {"last": ""}
        self.index = 0
        self.videos = []
        self.available = []
        self.last = ["", ""]
        self.get_available()

    def get_available(self):
        here = f"source/{self.subreddit.display_name}"
        flip = False
        for folder in [x[0] for x in os.walk(here)]:
            for file in os.listdir(folder):
                if flip and file.endswith(".mp4"):
                    self.available.append(f"{folder}/{file}")
                last = self.data.data["subreddits"][self.subreddit.display_name]["last"]
                if f"{folder}/{file}" == last or last == "":
                    flip = True
        print(f"{self.subreddit.display_name} has {len(self.available)} clips available.")

    def load_video(self, path):
        self.videos.append(VideoFileClip(path))

    def next_video(self):
        if len(self.available) > 0:
            self.index += 1
            print(self.index, len(self.available))
            if self.index >= len(self.available):
                print("heeeee")
                return None
            else:
                self.load_video(self.available[self.index])
                return self.videos[-1]
        else:
            return None

    def set_last(self):
        self.data.data["subreddits"][self.subreddit.display_name]["last"] = self.videos[-1].filename
        self.data.save_data()
