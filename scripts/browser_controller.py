import os
import time
import traceback
import zipfile

import pyperclip
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class BrowserController:

    def start_browser(self, profile_path=None):
        options = webdriver.ChromeOptions()
        if profile_path:
            profile_dir = profile_path.split('/')[-1]
            profile_path_without_dir = '/'.join(profile_path.split('/')[:-1])
            options.add_argument(f"user-data-dir={profile_path_without_dir}")  # Path to your chrome profile
            options.add_argument(f"--profile-directory={profile_dir}")
        self.driver = webdriver.Chrome(chrome_options=options)

    def start_firefox(self):
        self.driver = webdriver.Firefox()

    def youtube_send_comment(self, video_url, comment_text):
        try:
            self.driver.get(video_url)
        except:
            logger.info('Не удалось открыть страницу видео')
            return False

        for x in range(7):
            try:
                comment_area = self.driver.find_element_by_css_selector('[id="placeholder-area"]')
                comment_area.click()
                break
            except:
                self.driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                for x in range(1):
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)

        else:
            logger.info('Не удалось найти поле для ввода комментария')
            return False

        pyperclip.copy(comment_text)
        # pyperclip.copy(random.choice(cite))
        try:
            self.driver.find_element_by_css_selector('[id="contenteditable-root"]').send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            self.driver.find_element_by_css_selector('[id="submit-button"]').click()
        except:
            logger.info('Не удалось отправить комментарий')
            return False
        time.sleep(10)
        return True

    def youtube_check_comment(self, video_url, comment_text):
        try:
            self.driver.get(video_url)
        except:
            logger.info('Не удалось открыть страницу видео')
            return False

        for x in range(10):
            try:
                trigger = self.driver.find_element_by_css_selector('[id="trigger"]')
                break
            except:
                time.sleep(1)

        else:
            logger.info('Не удалось найти триггер')
            return False

        try:
            trigger.click()
        except:
            logger.info('Не удалось нажать на триггер')
            return False

        time.sleep(3)

        try:
            self.driver.find_element_by_css_selector('[class="yt-simple-endpoint style-scope yt-dropdown-menu"]').click()
        except:
            logger.info('Не удалось нажать на кнопку "Показать все комментарии"')
            return False

        for x in range(10):
            comments = self.driver.find_elements_by_css_selector('[id="content-text"]')
            if not comments:
                time.sleep(1)
                continue
            comments_text = [comment.text for comment in comments]
            if comment_text in comments_text:
                    return True
            time.sleep(1)
        else:
            logger.info('Не удалось найти комментарий')
            return False


    def close_browser(self):
        self.driver.close()


if __name__ == '__main__':
    driver = BrowserController(
        profile_name=r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\bot35\profile 35;91.229.79.73:45785@Selandreyslizh1:O7p5TdK').start_browser(
        proxy=True, headless=False)
    input('sdgsdgs')
