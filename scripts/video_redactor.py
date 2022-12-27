import os
import time
import traceback

from scripts.file_manager import FileManager


class VideoRedactor:

    def mirror_video(self, video_path, output_path=None):

        FileManager().copy_video_to_temp(video_path)
        temp_file_path = './videos/temp.mp4'
        ffmpeg_command = f'ffmpeg -y -i "{temp_file_path}" -c:v h264 -vf hflip "{video_path}"'
        os.system(ffmpeg_command)
        print('Закрываю видео')


    # def mirror_video_copy(self, video_path, output_path=None):
    #
    #     FileManager().copy_video_to_temp(video_path)
    #     time.sleep(1)
    #
    #     options = {"vcodec": "h264"}
    #
    #     inp_vi = ffmpeg.input('./videos/temp.mp4', kwargs=options)
    #     inp_au = ffmpeg.input('./videos/temp.mp4').audio
    #
    #     # overlay_file = ffmpeg.input('./in/images/Flushed_Face_Emoji_medium.png')
    #
    #     # print('Открываю видео')
    #     # delete video
    #     # try:
    #     #     os.remove(video_path)
    #     # except:
    #     #     traceback.print_exc()
    #     #     pass
    #     time.sleep(1)
    #
    #     inp = inp_vi.video.hflip()
    #     if output_path:
    #         out = ffmpeg.output(inp, inp_au, output_path).run()
    #     else:
    #         out = ffmpeg.output(inp, inp_au, video_path).run()
    #
    #     print('Закрываю видео')


if __name__ == '__main__':
    VideoRedactor().mirror_video(
        r'D:\git\selenium-upload-video-youtube\scripts\videos\test.mp4', r'D:\git\selenium-upload-video-youtube\scripts\videos\test2.mp4')
