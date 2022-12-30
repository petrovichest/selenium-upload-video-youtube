import os
import random
import time

from loguru import logger

from scripts.file_manager import FileManager
# from scripts.youtube_api import YoutubeApiController
from scripts.requests_controller import RequestsController
# from scripts.browser_controller import BrowserController
from scripts.random_russian_cite import GetRandomCite
from scripts.youtube_uploader_selenium import YouTubeUploaderSelenium

class YouTubeCommenter:


    def run(self):
        while True:
            accs_ready_to_comment = []
            accs_data = FileManager().read_accs_data()
            time.sleep(10)
            for one_acc_login in accs_data:
                accs_in_use = FileManager().read_accs_in_use()
                if one_acc_login in accs_in_use:
                    continue
                one_acc_data = accs_data.get(one_acc_login)
                last_comment = one_acc_data.get('last_comment')
                time_between_comments = one_acc_data.get('time_between_comments')
                status = one_acc_data.get('status')
                if not status:
                    continue
                if int(time.time()) - last_comment < time_between_comments:
                    continue
                logger.info(f'Аккаунт {one_acc_login} готов к комментированию')
                accs_ready_to_comment.append(one_acc_login)

            if not accs_ready_to_comment:
                continue

            search_queries = FileManager().read_start_search_query()
            videos_urls = []
            for one_query in search_queries:
                one_query_videos = RequestsController().youtube_parse_videos_by_search_text(one_query)
                comment_videos_blacklist = FileManager().read_comment_videos_black_list()
                one_query_videos = [x for x in one_query_videos if x not in comment_videos_blacklist]
                videos_urls.extend(one_query_videos)

            if not videos_urls:
                logger.info(f'Нет видео для комментирования')
                continue

            for one_acc_login in accs_ready_to_comment:
                one_acc_profile = accs_data.get(one_acc_login)
                acc_profile_path = accs_data.get(one_acc_login).get('firefox_path')
                video_url = random.choice(videos_urls)
                videos_urls.remove(video_url)
                FileManager().write_comment_videos_black_list(video_url)

                comments_base = FileManager().read_comments_base()
                comment = random.choice(comments_base)
                random_cite = GetRandomCite().return_cite()
                final_comment = f'{comment}\n{random_cite}'

                FileManager().write_accs_in_use(one_acc_login)
                browser_controller = YouTubeUploaderSelenium(acc_profile_path)

                send_comment_result = browser_controller.youtube_send_comment(video_url, final_comment)
                browser_controller.browser.quit()
                FileManager().delete_accs_in_use(one_acc_login)

                if not send_comment_result:
                    logger.info(f'Комментарий не отправлен. Аккаунт: {one_acc_login}')
                    continue

                one_acc_profile['last_comment'] = int(time.time())
                FileManager().write_accs_data(one_acc_login, one_acc_profile)
                logger.info(f'Комментарий отправлен на аккаунте {one_acc_login} на видео {video_url}')


