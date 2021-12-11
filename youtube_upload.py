import os
import re
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class YoutubeUpload:

    def __init__(self):
        chrome_options = Options()
        user_path = r'C:\Users\kate\AppData\Local\Google\Chrome\User Data\YoutubeUploader'
        user_profile = 'Profile 10'

        with open('res/tags.txt', 'r', encoding='utf-8') as f:
            self.videos_tags = [x.strip().replace(' ', '') for x in f.read().split('\n') if x]
        with open('res/videos_counter.txt', 'r', encoding='utf-8') as f:
            self.video_number = int(f.read().strip())
        chrome_options.add_argument(f'user-data-dir={user_path}')
        chrome_options.add_argument(f'--profile-directory={user_profile}')

        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get('https://studio.youtube.com/channel/')

    def upload_video(self, video_data, video_path):
        video_title =  video_data
        if not video_title:
            return False

        # self.driver.get('https://studio.youtube.com/channel/')
        time.sleep(2)
        for x in range(2):
            try:
                upload_btn = self.driver.find_element_by_css_selector('[id="upload-icon"]')
                upload_btn.click()
                break
            except:
                # self.driver.get('https://studio.youtube.com/channel/')
                time.sleep(1)
        else: return False
        for sdasdfs in range(10):
            try:
                file_input_element = self.driver.find_element_by_css_selector('[name="Filedata"]')
                break
            except:
                time.sleep(1)
        else:
            return False
        file_input_element.send_keys(f'{video_path}')
        for x in range(15):
            try:
                self.driver.find_element_by_css_selector('[id="textbox"]')
                break
            except:
                time.sleep(1)

        video_name_input = self.driver.find_elements_by_css_selector('[id="textbox"]')[0]
        video_title =  f'Лучшие ТикТок видео #{self.video_number} | Самые веселые TikTok видео 2021 #Shorts'
        video_description_input = self.driver.find_elements_by_css_selector('[id="textbox"]')[1]
        for x in range(3):
            try:
                kids_radio_btn = self.driver.find_element_by_css_selector('[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')
                kids_radio_btn.click()
                break
            except:
                time.sleep(1)
        else:
            return False

        also_params = self.driver.find_element_by_css_selector('[id="toggle-button"]')
        also_params.click()
        time.sleep(1)

        video_tags_input = self.driver.find_element_by_css_selector('[placeholder="Добавьте тег"]')

        video_name_input.click()
        time.sleep(0.5)
        video_name_input.clear()
        time.sleep(0.5)
        video_name_input.clear()
        video_name_input.send_keys(video_title)
        video_tags = ','.join(self.videos_tags)
        video_tags_input.send_keys(video_tags)
        video_description_input.click()
        # video_description_input.send_keys(f'Мой телеграмм канал с красивыми девушками - https://t.me/only_private \n\n\n\n\n\n #{" #".join(self.videos_tags)}')

        video_playlist = self.driver.find_element_by_css_selector('[placeholder="Выберите плейлист"]')
        video_playlist.click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector('[id="checkbox-label-0"]').click()
        self.driver.find_element_by_css_selector('[class="action-buttons style-scope ytcp-playlist-dialog"]').find_element_by_css_selector('[class="done-button action-button style-scope ytcp-playlist-dialog"]').click()
        # video_tags_input.send_keys(video_tags)

        print(video_path)
        print(video_title)
        print(video_tags)
        print()

        for x in range(3):
            next_button = self.driver.find_element_by_css_selector('[id="next-button"]')
            next_button.click()
            time.sleep(2)
        public_radio_btn = self.driver.find_element_by_css_selector('[name="PUBLIC"]')
        public_radio_btn.click()
        done_button = self.driver.find_element_by_css_selector('[id="done-button"]')
        done_button.click()

        with open('bl.txt', 'a', encoding='utf-8') as f:
            f.write(f'{video_title}\n')

        for x in range(360):
            try:
                upload_progress = self.driver.find_elements_by_css_selector('[id="dialog-title"]')[-1].text
                if 'Обработка видео' in upload_progress:
                    upload_progress = self.driver.find_elements_by_css_selector(
                        '[class="progress-label style-scope ytcp-video-upload-progress"]')[-1].text
            except:
                upload_progress = self.driver.find_elements_by_css_selector('[class="progress-label style-scope ytcp-video-upload-progress"]')[-1].text

            try:
                if 'Видео опубликовано' in upload_progress or 'Проверка завершена' in upload_progress:
                    print('Video uploaded')
                    self.driver.find_elements_by_css_selector('[class="label style-scope ytcp-button"]')[-1].click()
                    self.video_number += 1
                    with open('res/videos_counter.txt', 'w') as f:
                        f.write(f'{self.video_number}')
                    return True
                else:
                    time.sleep(1)
            except:
                time.sleep(1)

        else:
            try:
                done_button = self.driver.find_element_by_css_selector('[id="done-button"]')
                done_button.click()
                time.sleep(5)
            except:
                self.driver.find_elements_by_css_selector('[class="label style-scope ytcp-button"]')[-1].click()
                pass

if __name__ == '__main__':
    pr = YoutubeUpload()
    pr.upload_video(f'{os.getcwd()}/6af15d051c_480_mp4.mp4')