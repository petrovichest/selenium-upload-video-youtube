from bs4 import BeautifulSoup
import requests
from loguru import logger


class TikTokDownloadOnlineApi:
    # https://tiktokdownload.online


    def get_url_video_without_watermark(self, video_url):

        url = "https://tiktokdownload.online/abc?url=dl"

        payload = f"id={video_url}"
        headers = {
            'authority': 'tiktokdownload.online',
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': ''
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        url_element = soup.select('[class*="without_watermark"]')
        try:
            video_without_watermark_url = url_element[0]['href']
        except:
            logger.info('video_without_watermark_url not found')
            return False

        logger.info(video_without_watermark_url)
        return video_without_watermark_url

    def get_bytes_by_video_url(self, video_url):
        r = requests.get(video_url)
        return r.content

if __name__ == '__main__':
    video_without = TikTokDownloadOnlineApi().get_url_video_without_watermark('https://www.tiktok.com/@yanswya/video/7175575794352278827')
    TikTokDownloadOnlineApi().get_bytes_by_video_url(video_without)