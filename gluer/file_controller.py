import json
import os


class FileController:

    def __init__(self, folder_path=None):

        if not folder_path:
            self.folder_path = os.getcwd()
        self.folder_path = folder_path

    def get_video_number(self):
        try:
            os.mkdir('./res')
        except:
            pass

        try:
            with open(f"./res/video_number.txt", "r") as f:
                video_number = f.read().split('\n')[0]
        except:
            video_number = 1

        return int(video_number)

    def save_video_number(self, number):
        try:
            os.mkdir('./res')
        except:
            pass

        with open(f"./res/video_number.txt", "w") as f:
            f.write(f'{number}')

    def save_video(self, video_name, video_bytes):
        try:
            os.mkdir('./videos')
        except:
            pass
        with open(f"./videos/{video_name}.mp4", "wb") as out:
            out.write(video_bytes)

    def save_video_name_and_description(self, file_name, description):
        try:
            os.mkdir('./res')
        except:
            pass

        try:
            with open('./res/videos_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {}

        data[file_name] = description
        with open('./res/videos_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_description_by_videoname(self, videoname):
        try:
            with open(f'{self.folder_path}/res/videos_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            return False

        try:
            return data[videoname]
        except:
            return False

    def read_bl(self):
        try:
            with open('./res/bl.txt', 'r', encoding='utf-8') as f:
                bl = [x for x in f.read().split('\n') if x]
        except:
            bl = []
        return bl

    def write_bl(self, video_name):
        with open('./res/bl.txt', 'a', encoding='utf-8') as f:
            f.write(f'{video_name}\n')
if __name__ == '__main__':
    # FileManager().save_video_name_and_description('sdsdgasdgasdha.mp4', 'ЛУшие приколы про котиков')
    print(FileController().get_description_by_videoname('sdsdgasdgasdha.mp4'))