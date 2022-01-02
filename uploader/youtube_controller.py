import os
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from uploader.file_video_manager import FileVideoManager
from uploader.deemojify import deEmojify
from scripts.browser_controller import BrowserController
from scripts.data_controller import DataController


class YoutubeUpload:

    def __init__(self, acc_data, video_type='short'):
        self.acc_data = acc_data
        user_path = acc_data.get('profile_path')
        self.videos_tags = acc_data.get('tags')
        self.category = acc_data.get('category')
        self.video_type = video_type
        self.video_title = acc_data.get(f'title_{video_type}')
        self.video_number = acc_data.get(f'{video_type}_counter')

        self.driver = BrowserController(profile_name=user_path).start_browser(proxy=False, headless=False)
        self.driver.get('https://studio.youtube.com/channel/')

    def upload_video(self, video_data, video_path):
        if not video_data:
            return False

        videos_data_path = video_path.replace(video_data, '').replace(f'/{self.video_type}/{self.category}', '')
        video_description = FileVideoManager(folder_path=videos_data_path).get_description_by_videoname(video_data)[:4998]

        if video_description == False:
            with open('./uploader/res/bl.txt', 'a', encoding='utf-8') as f:
                f.write(f'{video_data}\n')
            return False

        video_description = deEmojify(video_description)

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
        for x in range(60):
            try:
                self.driver.find_element_by_css_selector('[id="textbox"]')
                break
            except:
                time.sleep(1)

        video_name_input = self.driver.find_elements_by_css_selector('[id="textbox"]')[0]
        # video_title =  f'Лучшие ТикТок видео #{self.video_number} | Самые веселые TikTok видео 2021 #Shorts'
        video_title =  self.video_title.replace('{counter}', str(self.video_number))

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

        # try:
        #     error_message = self.driver.find_element_by_css_selector('[class="error-details style-scope ytcp-uploads-dialog"]').text
        #     print(error_message)
        #     return False
        # except:
        #     pass
        also_params = self.driver.find_element_by_css_selector('[id="toggle-button"]')
        also_params.click()
        time.sleep(1)

        video_tags_input = self.driver.find_element_by_css_selector('[placeholder="Добавьте тег"]')

        video_name_input.click()
        time.sleep(0.5)
        video_name_input.clear()
        time.sleep(0.5)
        for dfsfs in range(5):
            video_name_input.clear()
            video_name_input.send_keys(video_title)
            video_name_input_text = video_name_input.text
            if video_name_input_text == video_title:
                break
            else:
                time.sleep(1)
        video_tags = ','.join(self.videos_tags)
        video_tags_input.send_keys(video_tags)
        video_description_input.click()

        action = ActionChains(self.driver)
        # action.send_keys(f'Участвуй в бесплатном розыгрыше призов -  https://clck.ru/ZPjTe \n {video_description}')
        for one_fragment in video_description.split('|NEWROW|'):
            action.send_keys(f'{one_fragment}')
            action.send_keys(Keys.ENTER)
        action.perform()

        # video_description_input.send_keys(video_description)
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

        with open('./uploader/res/bl.txt', 'a', encoding='utf-8') as f:
            f.write(f'{video_data}\n')

        for x in range(60*30):
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
                    self.video_number += 1
                    if self.video_type == 'long':
                        self.acc_data['long_last_update'] = int(time.time())
                    self.acc_data[f'{self.video_type}_counter'] = self.video_number
                    DataController().write_acc_data(acc_data=self.acc_data)
                    self.driver.find_elements_by_css_selector('[class="label style-scope ytcp-button"]')[-1].click()

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

        return True

if __name__ == '__main__':
    pr = YoutubeUpload()
    pr.upload_video(f'{os.getcwd()}/6af15d051c_480_mp4.mp4')