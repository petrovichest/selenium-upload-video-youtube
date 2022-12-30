import time

import requests
from loguru import logger

from scripts.file_manager import FileManager


class TikTokApi:

    def get_videos_by_search_query(self, search_query, videos_count) -> list:
        videos = []
        offset = 0
        videos_downloaded = FileManager().read_downloaded_videos()
        while True:
            if len(videos) >= videos_count:
                break
            logger.info(f'Получение видео по хэштегу {search_query} с offset {offset}')
            url = f"https://www.tiktok.com/api/search/general/full/?keyword={search_query}&offset={offset}"

            payload = {}
            headers = {
                'authority': 'www.tiktok.com',
                'accept': '*/*',
                'accept-language': 'ru,en;q=0.9',
                'cookie': '_ttp=297heEr29UlKP5CyLOjL4t4nBq2; tiktok_webapp_theme=light; cookie-consent={%22ga%22:false%2C%22af%22:false%2C%22fbp%22:false%2C%22lip%22:false%2C%22bing%22:false%2C%22ttads%22:false%2C%22reddit%22:false%2C%22version%22:%22v8%22}; __tea_cache_tokens_1988={%22_type_%22:%22default%22%2C%22user_unique_id%22:%227166187372839814662%22%2C%22timestamp%22:1668523084617}; tt_csrf_token=cauFtA5X-7m-HB9jR3zfRPTaAPVPNwhLTiuA; tt_chain_token=S/tL7KVeeV//EkJP7LxTJg==; _abck=F77446DD8563132BCF6450CF2B5AC51A~0~YAAQNb85VhI2tROFAQAAopneKwltNeQL0osmsa6juB6kuGrZY+ZjbtuHH3YNt26FjKda9aG4rsR9RPqy/qCI6EB0CKUZXk5pGhGhsp20fNucHuYVhGZrfnucb4UYqPna6h1YgthVIGljRRCnOD38Xl87VTSlN0sGfB0WhIWr8eJjFh4NKPfqTRfpZEWuSm8hOdh1rAROljdMFbWKcXrjTJ9n04j47CLJk3RM2hlRsr4oE9XFlbzWpLLotmzoR2SdOa6muPlwEApzjhbY7RfeYm76LmJb0Cm0/wX62gjGXmzDrpcsyx5YLu/nZx6JT7M31ntN660tw/f/cGeyLah/C142dfwNXqgAwLZ4GLMeWV930wg9kImGUBtg3GwljpBgAXXAEDxRYJ6zRMeUrc+iP/IOOSnIXXkd~-1~-1~-1; bm_sz=4779F076A1D144482F7776870E2ACAFA~YAAQNb85VhU2tROFAQAAopneKxL/X5M4TBp1fY9OvPq5HOccBL5DTMluf+eBKu3fPM7rVjYwHk2oLnhsMj6T8ycUoZr6moBxbYvtbo2Vj0aoXy/3MhQPlFXQSRisJm2dByD5PB4WFVHnqHPNbH1uHd2lZgJaxFDo5nxhaYChxQQRY0IYGsnmmGlHAGsrY5naL6dFw0Bhlckh4QsNALRIbam9mijQxM8w7QY1gh7cGuDYtgo6mwo2uQVD6/okYip39t2WRQu+b8trRDvFDvCKgoNZsIkeAxEpPDXgos9A+6fV7I0=~3354933~4534324; ak_bmsc=EDA508AEEE01966492BEA94975EA6BDC~000000000000000000000000000000~YAAQNb85Vhs2tROFAQAAxqDeKxKT+gSowRFkXiuMx78fM/GUlK69kznk/PTHbOImPW/EyGW8Z/4s/d/uCHgZVpGRsJ2Ito7uARc6ZkBFMSMA+o499JS0R28Se1aGCqzayW+QvssproTNnQxZoQlbBV8kBBpC4n4lmO8h3+FSUKpGtXE8KO/61NeWTBFiVV52JDKp/NarRakhEMA0RTPl5JtNVd4S1R5FYkHzgdUrjZ63gA9Fbs40h8AX+bHullnltDxrN5or/zCpp4OwdBACK9PZOJ6683SaTdi1T93K+DeZocztZKS0/hZowW6GP17p7Y9tjebu/wzIGePcmE/3aHdX+HdTjxMyhjh8uWqrb5lFcXiH4xcdj4xO4jXhIo209S2CSKA7juAi68PwIGCAvCLIvkbQ0vNe7hScSu5BgUrlEN1XJy8xVk47MpgYUCFH39cu083nSS/uvaREfqlZt3cdzLpihCciFnG5eazn8C4UuvDysKu920I=; bm_sv=28297C0AA42DF335DFD5237DF2FAEFCC~YAAQNb85Voc2tROFAQAAnZTfKxL9r7ZezvJGDtA+Jrw9x8+OIIpdfXjiAFhQiWSGDGIgwcMPkwPMwRD2QrNBkcX0WLeKIcn+/aVtgNGK0aixKWTeEbTIbscyM7cttnvPyA85y76kQKBa6i3vFa2Id5v0lYGtj0gDy5x6kV1C3GbyGw8qZBcLAzEZgjHlugwSqfUWwTFT2yXdrXyEDmHlbWhJX3zg9hAYW+O6joaSp+1llsnySKXdT2Eb7EuwOvM8~1; ttwid=1%7CTwE184vxcSZy7-kSVu6OfVm8dYSHmaEiMloB2KaTc9k%7C1671478352%7C71021017789cea233411d53c9aabee3c340f02c7dfaf4fd6d8b4b788192b07dc; msToken=b-OV1rApKFXFbl88szO_ArHKSswIeugHO3biWnLvOje8XDeZRpwpfbjele7ZIcKBdMXI5iQx9-asF0CV2GuRfCiSu_sP-ooXkrSjGy_l6roka-I1HCbuCw473D3po2lTEw6HxVcqWvs2aLNJ; msToken=b-OV1rApKFXFbl88szO_ArHKSswIeugHO3biWnLvOje8XDeZRpwpfbjele7ZIcKBdMXI5iQx9-asF0CV2GuRfCiSu_sP-ooXkrSjGy_l6roka-I1HCbuCw473D3po2lTEw6HxVcqWvs2aLNJ; _abck=F77446DD8563132BCF6450CF2B5AC51A~-1~YAAQTb85VsYvZQiFAQAACPHrKwlzVk1JbIZ8TRprxzLrH8T/w/8Bm7Tkdrb1fyiMPY8ugvMOWVX/PJruIxveItd8J76RW2k512f9/ft6HeGg39LzDvSLlHO25615PC9nXsvuOHJATQDsnfBqpmD0GNX+9VWqbqByh/W7Igv3sCnOm3avcO3e7gvNf4hB511SHuzjw7Zjew0AsraYPBLNzEX9JW5gWakETbvFK02uybhLwnsyvEX3NQjGcPr8KUydiE2BBXviJJ3o3X1bz9epBrvs3B4QXdIbWIT2Fr4dottFTHMSZRUGAv7j9/bnPu/W8RpaaHCoQOPDQilZn4aGgClrihJoiR9T66mebZ8IV6TZg2tufKwYstiamFr/1K0x0PO1bvU7JWefAEsrzI02dCGddu5XC+aW~0~-1~-1; bm_sz=E596E0922CC3C5697FA4F34EAB9671F6~YAAQTb85VossZQiFAQAAjTznKxJ+wc+Z0Oj2if7f14nGPz1BxUTUtbo2SMM+NE8pt8iLmjx5uv0YE/ub5nCVD6NG/hjsYUBiEf2NIGQOc+DPCLP5vIL/AusnVnEDW+XlRgSuX38MiLYlaXJf0B576VNXyYc3n9VFcTXivomIemR86r+XlMdRR/G4urHJRWQ6u6FNDiwZ//9w4+jF50sfAi5QKzJXHHIgo2HMrWfk/esIYSKQD7m998hNGhsuiL1AGVFGKy9RRsYK1ZdAZazPlCk2S/xZRlSei4bo7Gvtw1Zfjwc=~3752499~4403252',
                'sec-ch-ua': '"Chromium";v="106", "Yandex";v="22", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.818 Yowser/2.5 Safari/537.36'
            }
            # time.sleep(5)
            response = requests.request("GET", url, headers=headers, data=payload)

            try:
                response_json = response.json()
            except:
                return videos

            resp_data = response_json.get('data')
            if not resp_data:
                logger.info(f'Не удалось получить данные\nСобрано видео: {len(videos)}')
                return videos
            for one_video in response_json.get('data'):
                one_video_data = {}
                try:
                    video_id = one_video.get('item').get('video').get('id')
                except:
                    continue

                if video_id in videos_downloaded:
                    continue

                video_desc = one_video.get('item').get('desc')
                author_name = one_video.get('item').get('author').get('uniqueId')

                one_video_data['id'] = video_id
                one_video_data['desc'] = video_desc
                one_video_data['author_name'] = author_name
                videos.append(one_video_data)


            offset += 12
        logger.info(f'Видео по хэштегу {search_query} получены')
        return videos

if __name__ == '__main__':
    TikTokApi().get_videos_by_search_query('funny cats', 100)