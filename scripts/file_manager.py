import json
import os


class FileManager:
    def __init__(self):
        try:
            os.mkdir('./res')
        except:
            pass

        try:
            os.mkdir('./res/data')
        except:
            pass

        try:
            os.mkdir('./videos')
        except:
            pass

        try:
            os.mkdir('./videos/short')
        except:
            pass

    def read_downloaded_videos(self):
        try:
            with open('./res/data/downloaded_videos.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read() if x]
        except:
            data = []

        return data

    def write_downloaded_videos(self, data):
        with open('./res/data/downloaded_videos.txt', 'a', encoding='utf-8') as f:
            f.write(f'{data}\n')

    def read_published_videos(self):
        try:
            with open('./res/data/published_videos.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read() if x]
        except:
            data = []

        return data

    def write_published_videos(self, data):

        with open('./res/data/published_videos.txt', 'a', encoding='utf-8') as f:
            f.write(f'{data}\n')

    def read_accs_json(self):
        with open('./res/accs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def read_videos_data(self):
        try:
            with open('./res/data/videos_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {}

        return data

    def write_videos_data(self, data: dict):
        videos_data = self.read_videos_data()
        videos_data.update(data)
        with open('./res/data/videos_data.json', 'w', encoding='utf-8') as f:
            json.dump(videos_data, f, ensure_ascii=False, indent=4)

    def get_video_data(self, video_id):
        videos_data = self.read_videos_data()
        return videos_data.get(video_id)

    def delete_videos_data(self, data):
        videos_data = self.read_videos_data()
        for video in data:
            videos_data.pop(video)
        with open('./res/data/videos_data.json', 'w', encoding='utf-8') as f:
            json.dump(videos_data, f, ensure_ascii=False, indent=4)

    def read_accs_data(self):
        with open('./res/accs_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def write_accs_data(self, acc_login, data):
        accs_data = self.read_accs_data()
        accs_data[acc_login] = data
        with open('./res/accs_data.json', 'w', encoding='utf-8') as f:
            json.dump(accs_data, f, ensure_ascii=False, indent=4)

    def save_video(self, video_id, video_bytes, category):
        try:
            os.mkdir(f'./videos/short/{category}')
        except:
            pass

        with open(f'./videos/short/{category}/{video_id}.mp4', 'wb') as f:
            f.write(video_bytes)