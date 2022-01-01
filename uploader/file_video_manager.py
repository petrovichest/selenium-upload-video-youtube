import json
import os


class FileVideoManager:

    def __init__(self, folder_path=None):

        if not folder_path:
            self.folder_path = os.getcwd()
        self.folder_path = folder_path


    def get_description_by_videoname(self, videoname):
        try:
            with open(f'{self.folder_path}/videos_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            return False

        try:
            return data[videoname]
        except:
            return False

if __name__ == '__main__':
    # FileManager().save_video_name_and_description('sdsdgasdgasdha.mp4', 'ЛУшие приколы про котиков')
    print(FileVideoManager().get_description_by_videoname('sdsdgasdgasdha.mp4'))