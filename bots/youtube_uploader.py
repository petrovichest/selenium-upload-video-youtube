import os
import time

from loguru import logger

from scripts.file_manager import FileManager
from scripts.youtube_api import YoutubeApiController


class YouTubeUploader:

    uploaders = {}

    def init_all_accs(self):
        all_accs_data = FileManager().read_accs_data()
        for one_acc in all_accs_data:
            acc_status = all_accs_data.get(one_acc).get('status')
            if not acc_status:
                continue
            acc_client_id = all_accs_data.get(one_acc).get('client_id')
            acc_secret_id = all_accs_data.get(one_acc).get('secret_id')
            self.uploaders[one_acc] = YoutubeApiController(acc_client_id, acc_secret_id)

    def run(self):
        self.init_all_accs()
        while True:
            accs_data = FileManager().read_accs_data()
            for one_acc_login in self.uploaders:
                one_acc_data = accs_data.get(one_acc_login)
                acc_name = one_acc_data.get('acc_name')
                category = one_acc_data.get('category')
                short_counter = one_acc_data.get('short_counter')
                video_title = one_acc_data.get('title_short').replace('{counter}', str(short_counter))
                video_tags = one_acc_data.get('tags')
                last_upload_short = one_acc_data.get('last_upload_short')
                time_between_posts = one_acc_data.get('time_between_posts')

                if int(time.time()) - last_upload_short < time_between_posts:
                    continue

                videos_directory = f'{os.getcwd()}/videos/short/{category}'
                uploaded_videos = FileManager().read_published_videos()
                try:
                    available_videos = [x.split('.')[0] for x in os.listdir(videos_directory)]
                except:
                    time.sleep(10)
                    continue

                for video_name in available_videos:
                    if video_name in uploaded_videos:
                        continue
                    video_data = {}
                    video_data_raw = FileManager().get_video_data(video_name)
                    video_data.update(video_data_raw)
                    video_data['title'] = video_title
                    video_data['tags'] = video_tags
                    video_path = f'{videos_directory}/{video_name}.mp4'
                    upload_result = self.uploaders[one_acc_login].upload_video(video_data, video_path)

                    if "Quota" == upload_result:
                        one_acc_data["last_upload_short"] = int(time.time()) + 3600 * 3
                        FileManager().write_accs_data(acc_name, one_acc_data)
                        logger.info(f'Получена квота на загрузку видео, ожидаем 3 часа')
                        break
                    elif "Error" == upload_result:
                        one_acc_data["last_upload_short"] = int(time.time())
                        FileManager().write_accs_data(acc_name, one_acc_data)
                        logger.info(f'Ошибка загрузки видео')
                        break
                    elif "Success" == upload_result:
                        one_acc_data['short_counter'] = short_counter + 1
                        one_acc_data['last_upload_short'] = int(time.time())
                        FileManager().write_accs_data(acc_name, one_acc_data)
                        FileManager().write_published_videos(video_name)
                        FileManager().delete_video(video_path)
                        logger.info(f'Видео загружено: {video_name}')
                        break
                    else:
                        logger.error(f'Error: {upload_result}')
                        one_acc_data['last_upload_short'] = int(time.time())
                        FileManager().write_accs_data(acc_name, one_acc_data)
                        break


            time.sleep(10)
