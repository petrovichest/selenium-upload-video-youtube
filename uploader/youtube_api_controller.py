import time

from youtube_upload.client import YoutubeUploader

from scripts.data_controller import DataController
from uploader.file_video_manager import FileVideoManager


class YoutubeApiController:

    # token = 'AIzaSyAtLIgVM1vMjRLWHiNfrqW-j2boV9XdxLs'
    client_id = '745464782598-s2mcfk3bmpi4o0i24mqqt4iiqr414reo.apps.googleusercontent.com'
    secret_id = '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'
    def __init__(self, video_type='short'):
        self.video_type = video_type
        self.uploader = YoutubeUploader(client_id=self.client_id, client_secret=self.secret_id)
        self.uploader.authenticate()

    def init_account_data(self, acc_data):
        self.acc_data = acc_data
        user_path = acc_data.get('profile_path')
        self.videos_tags = acc_data.get('tags')
        self.category = acc_data.get('category')
        self.video_title = acc_data.get(f'title_{self.video_type}')
        self.video_number = acc_data.get(f'{self.video_type}_counter')

    def test(self):
        uploader = YoutubeUploader(client_id=self.client_id, client_secret=self.secret_id)
        uploader.authenticate()

        options = {
            "title": self.video_title,  # The video title
            "description": "Example description",  # The video description
            "tags": ["tag1", "tag2", "tag3"],
            # "categoryId": "22",
            "privacyStatus": "private",  # Video privacy. Can either be "public", "private", or "unlisted"
            "kids": False,  # Specifies if the Video if for kids or not. Defaults to False.
            # "thumbnailLink": "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg"
            # Optional. Specifies video thumbnail.
        }

        uploader.upload(r"D:\git\selenium-upload-video-youtube\videos\short\animals funny\6985223154612358406.mp4", options)

    def upload_video(self, video_data, video_path):
        if not video_data:
            return False

        videos_data_path = video_path.replace(video_data, '').replace(f'/{self.video_type}/{self.category}', '')
        video_description = FileVideoManager(folder_path=videos_data_path).get_description_by_videoname(video_data)[:4998]
        video_title = self.video_title.replace('{counter}', str(self.video_number))

        if video_description == False:
            with open('./uploader/res/bl.txt', 'a', encoding='utf-8') as f:
                f.write(f'{video_data}\n')
            return False

        options = {
            "title": video_title,  # The video title
            "description": video_description,  # The video description
            "tags": self.videos_tags,
            # "categoryId": "22",
            "privacyStatus": "private",  # Video privacy. Can either be "public", "private", or "unlisted"
            "kids": False,  # Specifies if the Video if for kids or not. Defaults to False.
            # "thumbnailLink": "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg"
            # Optional. Specifies video thumbnail.
        }


        self.uploader.upload(video_path, options)
        with open('./uploader/res/bl.txt', 'a', encoding='utf-8') as f:
            f.write(f'{video_data}\n')
        if self.video_type == 'long':
            self.acc_data['long_last_update'] = int(time.time())
        self.acc_data[f'{self.video_type}_counter'] = self.video_number
        DataController().write_acc_data(acc_data=self.acc_data)
        return True



if __name__ == '__main__':
    pr = YoutubeApiController()
    pr.test()