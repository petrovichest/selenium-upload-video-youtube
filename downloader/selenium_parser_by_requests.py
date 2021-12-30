import json
import time
import traceback

from seleniumwire import webdriver
from seleniumwire.utils import decode

from downloader.tiktok_controller import TiktokController


class SeleniumParserByRequests:



    def parse_videos_by_search(self, search_text, videos_count=24):
        self.driver = webdriver.Chrome()

        videos_page_count = videos_count // 12

        current_time = int(time.time())
        self.driver.get(f'https://www.tiktok.com/search?q={search_text}&t={current_time}')

        TiktokController().close_captcha(self.driver)

        for dfsf in range(videos_page_count):
            TiktokController().load_more(self.driver)

        all_videos_data = []
        events = self.driver.requests
        for event in events:
            try:
                event.url
            except:
                continue
            if 'm.tiktok.com/api/search/general/full/' in event.url:
                if event.response:
                    try:
                        response_bytes = decode(event.response.body,
                                                event.response.headers.get('Content-Encoding', 'identity'))
                        response_json = json.loads(response_bytes.decode(), strict=False)
                    except:
                        traceback.print_exc()
                        continue
                    videos_data_dict = response_json.get('data')
                    all_videos_data.append(videos_data_dict)

        self.driver.close()
        return all_videos_data

    def run(self):
        self.parse_videos_by_search(search_text='Животные', videos_count=300)







if __name__ == '__main__':
    SeleniumParserByRequests().run()