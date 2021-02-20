import time
import youtube_upload
import os

class MainClass:
    def __init__(self):
        self.videos_directory = r'E:\git_public\my_prods\tiktok-downloader-python-selenium\out'
        self.videos = os.listdir(self.videos_directory)
        with open('bl.txt', 'r', encoding='utf-8') as f:
            self.bl = [x.strip() for x in f.read().split('\n') if x]

    def run_apload_videos(self):
        uploader = youtube_upload.YoutubeUpload()
        # videos_data = csv_controller.csv_reader()
        videos_data_names = os.listdir(self.videos_directory)
        counts = 0
        for video_name in self.videos:
            if counts > 30:
                return
            if video_name in self.bl:
                continue
            video_path = f'{self.videos_directory}/{video_name}'
            if not uploader.upload_video(video_name, video_path):
                continue
            self.bl.append(video_name)
            with open('bl.txt', 'a', encoding='utf-8') as f:
                f.write(f'{video_name}\n')
            counts += 1
            time.sleep(60*10)


if __name__ == '__main__':
    pr = MainClass()
    pr.run_apload_videos()
    print('Complete')
