import os
import time

from loguru import logger

from scripts.file_manager import FileManager
from scripts.tiktok_api import TikTokApi
from scripts.tiktokdownload_online_api import TikTokDownloadOnlineApi


class TikTokDownloader:

    def run(self):
        accs_data = FileManager().read_accs_json()

        for one_acc in accs_data:
            acc_status = accs_data.get(one_acc).get('status')
            category = accs_data.get(one_acc).get('category')
            if not acc_status:
                continue

            videos_directory = f'{os.getcwd()}/videos/short/{category}'
            try:
                videos_directory_count = len(os.listdir(videos_directory))
            except:
                videos_directory_count = 0
            if videos_directory_count > 10:
                continue

            logger.info(f'Загружаем видео для аккаунта {one_acc}')

            tiktok_api = TikTokApi()
            videos_data = tiktok_api.get_videos_by_hashtag(category, videos_count=100)

            if not videos_data:
                logger.info(f'Не удалось получить список видео')
                continue

            for one_video_data in videos_data:
                video_id = one_video_data.get('id')
                video_author_name = one_video_data.get('author_name')
                video_url = f'https://www.tiktok.com/@{video_author_name}/video/{video_id}'

                video_without_watermark_url = TikTokDownloadOnlineApi().get_url_video_without_watermark(video_url)
                if not video_without_watermark_url:
                    logger.info('Видео без водяного знака не найдено')
                    time.sleep(10)
                    continue
                video_bytes = TikTokDownloadOnlineApi().get_bytes_by_video_url(video_without_watermark_url)
                if not video_bytes:
                    logger.info('Байты видео не были получены')
                    time.sleep(10)
                    continue

                FileManager().save_video(video_id, video_bytes, category)
                FileManager().write_videos_data(one_video_data)
                FileManager().write_downloaded_videos(video_id)
                logger.info(f'Видео {video_id} сохранено')
                time.sleep(10)

        logger.info('Загрузка видео завершена')





