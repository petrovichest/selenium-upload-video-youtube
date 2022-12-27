import os
import time

from loguru import logger

from scripts.file_manager import FileManager
from scripts.video_redactor import VideoRedactor

class VideosProcessor:

    def run(self):
        while True:
            time.sleep(10)
            videos_directory = f'{os.getcwd()}/videos/short'
            videos_categories = os.listdir(videos_directory)
            for one_category in videos_categories:
                category_directory = f'{videos_directory}/{one_category}'
                available_videos = [x.split('.')[0] for x in os.listdir(category_directory)]
                uploaded_videos = FileManager().read_published_videos()
                processed_videos = FileManager().read_processed_videos()
                downloaded_videos = FileManager().read_downloaded_videos()

                videos_to_process = [x for x in available_videos if x not in uploaded_videos and x not in processed_videos and x in downloaded_videos]
                logger.info(f'Videos to process: {len(videos_to_process)}')
                for video_name in videos_to_process:
                    logger.info(f'Processing video: {videos_to_process.index(video_name) + 1} in {len(videos_to_process)} {video_name} ...')
                    video_path = f'{category_directory}/{video_name}.mp4'
                    VideoRedactor().mirror_video(video_path)
                    FileManager().write_processed_videos(video_name)
                    logger.info(f'Video processed: {video_name}')
