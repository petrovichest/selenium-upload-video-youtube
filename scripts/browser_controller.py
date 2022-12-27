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

    def start_browser(self, profile_path):
        options = webdriver.ChromeOptions()
        profile_dir = profile_path.split('/')[-1]
        profile_path_without_dir = '/'.join(profile_path.split('/')[:-1])
        options.add_argument(f"user-data-dir={profile_path_without_dir}")  # Path to your chrome profile
        options.add_argument(f"--profile-directory={profile_dir}")
        self.driver = webdriver.Chrome(chrome_options=options)

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

    def close_browser(self):
        self.driver.close()


if __name__ == '__main__':
    driver = BrowserController(
        profile_name=r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\bot35\profile 35;91.229.79.73:45785@Selandreyslizh1:O7p5TdK').start_browser(
        proxy=True, headless=False)
    input('sdgsdgs')
