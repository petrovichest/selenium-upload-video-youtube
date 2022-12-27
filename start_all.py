from threading import Thread

from bots.tiktok_downloader import TikTokDownloader
from bots.youtube_uploader import YouTubeUploader
from bots.videos_processor import VideosProcessor
from bots.youtube_comment import YouTubeCommenter

if __name__ == '__main__':

    threads_list = [
        TikTokDownloader,
        YouTubeUploader,
        VideosProcessor,
        YouTubeCommenter
    ]
    for thread in threads_list:
        Thread(target=thread().run).start()

