import os, datetime


def get_video_url(post):
    return post.media['reddit_video']['fallback_url']


def get_audio_url(post):
    url = get_video_url(post)
    return url.split("DASH_")[0] + "DASH_audio.mp4"


class PostCrawler:
    def __init__(self, red, sub):
        self.subreddit = red.subreddit(sub)
        self.posts = []
        self.method = None
        self.period = None

    def crawl(self, **kwargs):
        all_posts = []
        self.method = kwargs["method"]
        self.period = kwargs["period"]
        print(self.method, self.period)
        for i, method in enumerate(["hot", "new", "top"]):
            if method == kwargs["method"]:
                methods = [lambda: self.subreddit.hot(), lambda: self.subreddit.new(), lambda: self.subreddit.top(kwargs["period"])]
                all_posts = methods[i]()
                print(all_posts)

        for post in all_posts:
            if post.media and 'reddit_video' in post.media and post.id+".mp4" not in self.get_all():
                self.posts.append(post)
        print(f"found {len(self.posts)} video posts")

    def get_all(self):
        all_vids = []
        for folder in [x[0] for x in os.walk(f"source/{self.subreddit.display_name}")]:
            for file in os.listdir(folder):
                if file.endswith(".mp4"):
                    all_vids.append(file)
        return all_vids

    def compile_all(self):
        for post in self.posts:
            self.compile_video(post)

    def compile_video(self, post):
        os.system("mkdir build")
        os.system("curl -o build/video.mp4 {}".format(get_video_url(post)))
        os.system("curl -o build/audio.mp4 {}".format(get_audio_url(post)))
        if self.subreddit.display_name not in os.listdir("source"):
            os.system(f"cd source && mkdir {self.subreddit.display_name}")
        dir_name = str(datetime.datetime.now()).split(" ")[0]+f"-{self.method}{'-'+self.period if self.method == 'top' else ''}"
        os.system(f"cd source/{self.subreddit.display_name} && mkdir {dir_name}")
        video_path = f"source/{self.subreddit.display_name}/{dir_name}/{post.id}.mp4"
        os.system("ffmpeg -y -i build/video.mp4 -i build/audio.mp4 -c:v copy -c:a aac -strict experimental "+video_path)
        print(video_path)
        os.system("rmdir /s /q build")
        print("compiled complete!")

