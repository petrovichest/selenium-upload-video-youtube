import time
import os

from uploader import youtube_controller
from scripts.data_controller import DataController

class YouTubeUploaderController:
    def run_upload_videos(self, acc_data,  video_type='short'):
        self.acc_name = acc_data.get('acc_name')
        self.category = acc_data.get('category')
        self.video_title = acc_data.get(f'title_{video_type}')
        self.videos_main_directory = f'D:/git/selenium-upload-video-youtube/videos'
        self.videos_directory = f'{self.videos_main_directory}/{video_type}/{self.category}'
        try:
            self.videos = os.listdir(self.videos_directory)
        except:
            return False
        for video_name in self.videos:
            with open('./uploader/res/bl.txt', 'r', encoding='utf-8') as f:
                self.bl = [x.strip() for x in f.read().split('\n') if x]
            if video_name in self.bl:
                video_path = f'{self.videos_directory}/{video_name}'
                try:
                    os.remove(video_path)
                except:
                    pass
                continue
            uploader = youtube_controller.YoutubeUpload(acc_data, video_type=video_type)
            video_path = f'{self.videos_directory}/{video_name}'
            if not uploader.upload_video(video_name, video_path):
                continue
            # with open('bl.txt', 'a', encoding='utf-8') as f:
            #     f.write(f'{video_name}\n')
            uploader.driver.close()
            return True

    def run(self):
        while True:
            accs_data = DataController().read_accs_json()
            for one_acc in accs_data:
                acc_status = accs_data.get(one_acc).get('status')
                if acc_status:
                    current_time = int(time.time())
                    if current_time > accs_data.get(one_acc).get('long_last_update') + (3600 * 24):
                        if not self.run_upload_videos(accs_data.get(one_acc), video_type='long'):
                            self.run_upload_videos(accs_data.get(one_acc))

                    else:
                        self.run_upload_videos(accs_data.get(one_acc))
            time.sleep(10*60)


if __name__ == '__main__':
    pr = YouTubeUploaderController()
    pr.run_upload_videos()
    print('Complete')
