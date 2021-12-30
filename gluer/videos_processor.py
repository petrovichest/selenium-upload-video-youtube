import os

from moviepy.editor import VideoFileClip, concatenate_videoclips

from gluer.file_controller import FileController
from gluer.time_converter import TimeConverter


class VideosProcessor:

    def __init__(self, work_dist_path):
        self.work_dist_path = work_dist_path

    def compose_videos(self, length=600):
        video_number = FileController().get_video_number()
        video_name = f'./videos/video_{video_number}.mp4'
        curren_length = 0
        videos = os.listdir(f'{self.work_dist_path}/videos')

        videos_to_concate = []
        videos_descriptions = ''
        for one_video in videos:
            if curren_length > length:
                break

            bl = FileController().read_bl()
            if one_video in bl:
                continue
            video_path = f'{self.work_dist_path}/videos/{one_video}'
            video_description = FileController(folder_path=self.work_dist_path).get_description_by_videoname(one_video)
            if not video_description:
                continue

            try:
                video = VideoFileClip(video_path)
                video = video.resize(newsize=(540, 960))
            except:
                continue

            video_length = video.duration
            video_start_time = TimeConverter().seconds_to_minutes(int(curren_length))
            videos_descriptions += f'{video_start_time} - {video_description}|NEWROW|'
            curren_length += video_length
            videos_to_concate.append(video)
            FileController().write_bl(one_video)

        final_clip = concatenate_videoclips(videos_to_concate)
        final_clip.write_videofile(video_name)
        FileController().save_video_name_and_description(file_name=video_name, description=videos_descriptions)
        FileController().save_video_number(video_number + 1)