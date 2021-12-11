import time
import youtube_upload
import os

class YouTubeUploader:
    def __init__(self):
        self.videos_directory = r'D:\git\tiktok-downloader-python-selenium\videos'
        self.videos = os.listdir(self.videos_directory)

    def run_apload_videos(self):
        uploader = youtube_upload.YoutubeUpload()
        # videos_data = csv_controller.csv_reader()
        videos_data_names = os.listdir(self.videos_directory)
        counts = 0
        for video_name in self.videos:
            if counts > 30:
                return
            with open('bl.txt', 'r', encoding='utf-8') as f:
                self.bl = [x.strip() for x in f.read().split('\n') if x]

            if video_name in self.bl:
                video_path = f'{self.videos_directory}/{video_name}'
                try:
                    os.remove(video_path)
                except:
                    pass
                continue
            video_path = f'{self.videos_directory}/{video_name}'
            if not uploader.upload_video(video_name, video_path):
                continue
            # with open('bl.txt', 'a', encoding='utf-8') as f:
            #     f.write(f'{video_name}\n')
            counts += 1
            time.sleep(60*10)


if __name__ == '__main__':
    pr = YouTubeUploader()
    pr.run_apload_videos()
    print('Complete')
