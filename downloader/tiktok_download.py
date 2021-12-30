import time

from TikTokApi import TikTokApi
from downloader.file_manager import FileManager
from downloader.selenium_parser_by_requests import SeleniumParserByRequests

class TikTokDownload:

    EXCEPTIONS = ['беларусь', 'бчб', 'живе', 'рб']

    def download_by_hashtag(self, hashtag, videos_count):
        api = TikTokApi.get_instance(
            custom_verifyFp='verify_kxexi3bp_0TKViOxa_wHgP_4q98_9Yh4_ZSWkpuTlhWOa')
        # api = TikTokApi.get_instance()
        device_id = api.generate_device_id()

        result_count = 100
        # hashtag_objects = api.search_for_hashtags(hashtag)

        tiktoks_data = SeleniumParserByRequests().parse_videos_by_search(search_text=hashtag, videos_count=videos_count)

        for one_tiktok_data in tiktoks_data:
            for one_tiktok in one_tiktok_data:
                one_tiktok = one_tiktok.get('item')
                if not one_tiktok:
                    continue
                time.sleep(1)
                description = one_tiktok['desc']
                for one_exception in self.EXCEPTIONS:
                    if one_exception in description.lower():
                        break
                else:
                    video_bytes = api.get_video_by_tiktok(one_tiktok, custom_device_id=device_id)
                    FileManager().save_video(video_name=one_tiktok['id'],category=hashtag, video_bytes=video_bytes)

                    FileManager().save_video_name_and_description(f'{one_tiktok["id"]}.mp4', description)

                continue



if __name__ == '__main__':
    TikTokDownload().download_by_hashtag("animals", videos_count=10)
