import json
import os


class FileManager:

    def __init__(self):
        try:
            os.mkdir('./videos')
        except:
            pass

        try:
            os.mkdir('./videos/short')
        except:
            pass

    def save_video(self, video_name, category, video_bytes):
        try:
            os.mkdir(f'./videos/short/{category}')
        except:
            pass

        with open(f"./videos/short/{category}/{video_name}.mp4", "wb") as out:
            out.write(video_bytes)

    def save_video_name_and_description(self, file_name, description):
        try:
            with open('./videos/videos_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {}

        data[file_name] = description
        with open('./videos/videos_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_description_by_videoname(self, videoname):

        try:
            with open('./videos/videos_data.json', 'r', encoding='utf-8') as f:
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