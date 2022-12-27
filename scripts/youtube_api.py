import time
import traceback

import googleapiclient.errors
from loguru import logger
from youtube_upload.client import YoutubeUploader


class YoutubeApiController:

    def __init__(self, client_id, client_secret):
        self.uploader = YoutubeUploader(client_id=client_id, client_secret=client_secret)
        self.uploader.authenticate()

    def upload_video(self, video_data, video_path):
        if not video_data:
            return False

        video_description = video_data.get('desc')
        video_title = video_data.get('title')
        video_tags = video_data.get('tags')

        options = {
            "title": video_title,  # The video title
            "description": video_description,  # The video description
            "tags": video_tags,
            # "categoryId": "22",
            "privacyStatus": "public",  # Video privacy. Can either be "public", "private", or "unlisted"
            "kids": False,  # Specifies if the Video if for kids or not. Defaults to False.
        }

        try:
            upload_result = self.uploader.upload(video_path, options)
        except googleapiclient.errors.ResumableUploadError:
            return "Quota"
        except:
            traceback.print_exc()
            return "Error"
        try:
            if upload_result[0].get('status').get('uploadStatus') == 'uploaded':
                return "Success"
            else:
                logger.info(f'Загрузка не произошла{upload_result}')
                return "Error"
        except:
            logger.info(f'Ошибка получения статуса{upload_result}')
            return "Error"




if __name__ == '__main__':
    pr = YoutubeApiController()
