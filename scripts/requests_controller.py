import re

import requests
from bs4 import BeautifulSoup


class RequestsController:

    def youtube_parse_videos_by_search_text(self, search_text):
        # url = f'https://www.youtube.com/results?search_query={search_text}&sp=EgYIAhABGAM%253D'
        url = f'https://www.youtube.com/results?search_query={search_text}&sp=CAMSBggDEAEYAw%253D%253D'
        response = requests.get(url)
        videos_urls = re.findall(r'/watch\?v=[\w-]+', response.text)
        videos_urls = [f'https://www.youtube.com{x}' for x in videos_urls]
        return videos_urls


if __name__ == '__main__':
    rc = RequestsController()
    print(rc.youtube_parse_videos_by_search_text('приколы'))