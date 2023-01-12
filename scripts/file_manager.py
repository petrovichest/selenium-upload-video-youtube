import json
import os
import random


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

        try:
            os.mkdir('./res/start_search_querry')
        except:
            pass

        try:
            os.mkdir('./res/comments_base')
        except:
            pass

    def read_downloaded_videos(self):
        try:
            with open('./res/data/downloaded_videos.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def write_downloaded_videos(self, data):
        with open('./res/data/downloaded_videos.txt', 'a', encoding='utf-8') as f:
            f.write(f'{data}\n')

    def read_published_videos(self):
        try:
            with open('./res/data/published_videos.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def write_published_videos(self, data):

        with open('./res/data/published_videos.txt', 'a', encoding='utf-8') as f:
            f.write(f'{data}\n')

    def read_accs_json(self):
        with open('./res/accs_data.json', 'r', encoding='utf-8') as f:
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
        videos_data[data['id']] = data
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

    def delete_video(self, video_path):
        try:
            os.remove(video_path)
        except:
            pass

    def copy_video_to_temp(self, video_path):
        with open(video_path, 'rb') as f:
            video_bytes = f.read()
        with open('./videos/temp.mp4', 'wb') as f:
            f.write(video_bytes)

    def read_processed_videos(self):
        try:
            with open('./res/data/processed_videos.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def write_processed_videos(self, data):
        with open('./res/data/processed_videos.txt', 'a', encoding='utf-8') as f:
            f.write(f'{data}\n')

    def read_comments_base_personal(self, acc_login):
        try:
            with open(f'./res/comments_base/{acc_login}.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def read_comments_base(self):
        try:
            with open('./res/comments_base/base.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def read_start_search_querry_personal(self, acc_login):
        try:
            with open(f'./res/start_search_querry/{acc_login}.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def read_start_search_query(self):
        try:
            with open('./res/start_search_querry/base.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def read_comment_videos_black_list(self):
        try:
            with open('./res/data/comment_videos_black_list.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def write_comment_videos_black_list(self, data):
        with open('./res/data/comment_videos_black_list.txt', 'a', encoding='utf-8') as f:
            f.write(f'{data}\n')


    def read_accs_in_use(self):
        try:
            with open('./res/data/accs_in_use.txt', 'r', encoding='utf-8') as f:
                data = [x for x in f.read().split('\n') if x]
        except:
            data = []

        return data

    def write_accs_in_use(self, acc):
        with open('./res/data/accs_in_use.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{acc}\n')

    def delete_accs_in_use(self, acc):
        accs_in_use = self.read_accs_in_use()
        for acc_in_use in accs_in_use:
            if acc_in_use == acc:
                accs_in_use.remove(acc_in_use)

        with open('./res/data/accs_in_use.txt', 'w', encoding='utf-8') as f:
            accs_in_use_to_write = '\n'.join(accs_in_use)
            f.write(accs_in_use_to_write)

    def get_random_kaomoji(self):
        with open('./res/comments_base/kaomoji.txt', 'r', encoding='utf-8') as f:
            data = [x for x in f.read().split('\n') if x]
        return random.choice(data)