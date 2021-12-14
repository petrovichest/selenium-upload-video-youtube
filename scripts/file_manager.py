import json
import os


class FileManager:

    def __init__(self, folder_path=None):

        if not folder_path:
            self.folder_path = os.getcwd()
        self.folder_path = folder_path


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

if __name__ == '__main__':
    # FileManager().save_video_name_and_description('sdsdgasdgasdha.mp4', 'ЛУшие приколы про котиков')
    print(FileManager().get_description_by_videoname('sdsdgasdgasdha.mp4'))