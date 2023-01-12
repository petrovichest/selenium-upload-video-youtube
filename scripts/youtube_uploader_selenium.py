import traceback
from pathlib import Path

import pyperclip
from selenium.webdriver.firefox.options import Options
from typing import DefaultDict, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
import json
import time
import logging
import platform
from loguru import logger


class YouTubeUploaderSelenium:

    def __init__(self, profile_path=None) -> None:

        self.profile_path = profile_path

        binary_location = r'C:/Program Files/Mozilla Firefox/firefox.exe'
        if profile_path:
            self.browser = webdriver.Firefox(firefox_profile=self.profile_path, firefox_binary=binary_location)
            logger.debug(f"Использую профиль {self.profile_path}")
        if not profile_path:
            self.browser = webdriver.Firefox(firefox_binary=binary_location)

        self.browser.set_window_position(4000, 200)


    def upload(self, video_path, video_data):
        try:
            upload_result = self.__upload(video_path, video_data)
            self.__quit()
            return upload_result
        except Exception as e:
            print(e)
            self.__quit()
            raise

    def __clear_field(self, field):
        for x in range(2):
            try:
                field.click()
                break
            except:
                self.hide_element()
                input("Не удалось нажать на поле. Нажмите Enter, чтобы продолжить")
        time.sleep(Constant.USER_WAITING_TIME)
        field.send_keys(Keys.CONTROL + 'a')
        time.sleep(Constant.USER_WAITING_TIME)
        field.send_keys(Keys.BACKSPACE)

    def __write_in_field(self, field, string, select_all=False):
        if select_all:
            self.__clear_field(field)
        else:
            field.click()
            time.sleep(Constant.USER_WAITING_TIME)

        field.send_keys(string, Keys.ENTER*2)

    def __upload(self, video_path, video_data) -> str:
        self.video_path = video_path
        self.video_description = video_data.get('desc')
        self.video_title = video_data.get('title')
        self.video_tags = video_data.get('tags')
        self.video_playlist = video_data.get('playlist')

        self.browser.get(Constant.YOUTUBE_URL)
        time.sleep(Constant.USER_WAITING_TIME)
        self.browser.get(Constant.YOUTUBE_UPLOAD_URL)
        time.sleep(Constant.USER_WAITING_TIME)
        absolute_video_path = str(Path.cwd() / self.video_path)
        for x in range(10):
            try:
                self.browser.find_element_by_css_selector(Constant.INPUT_FILE_VIDEO).send_keys(
                    absolute_video_path)
                break
            except:
                traceback.print_exc()
                time.sleep(Constant.USER_WAITING_TIME)
        logger.debug('Attached video {}'.format(self.video_path))

        uploading_status_container = None
        for x in range(5):
            try:
                uploading_status_container = self.browser.find_element_by_css_selector(
                    Constant.UPLOADING_STATUS_CONTAINER)
                break
            except:
                uploading_status_container = None
        else:
            logger.error('Could not find uploading status container')
            return "Error"
        time.sleep(Constant.USER_WAITING_TIME)

        for x in range(15):
            try:
                title_field, description_field = self.browser.find_elements_by_css_selector(Constant.TEXTBOX_ID)
                if title_field and description_field:
                    break
            except:
                time.sleep(Constant.USER_WAITING_TIME)
                continue
        else:
            return "Error"

        self.__write_in_field(
            title_field, self.video_title, select_all=True)
        logger.debug('The video title was set to \"{}\"'.format(
            self.video_title))

        video_description = self.video_description
        video_description = video_description.replace("\n", Keys.ENTER).replace('@', '')
        if video_description:
            self.__write_in_field(description_field, video_description, select_all=True)
            logger.debug('Description filled.')

        kids_section = self.browser.find_element_by_css_selector(Constant.NOT_MADE_FOR_KIDS_LABEL)
        time.sleep(Constant.USER_WAITING_TIME)
        for x in range(5):
            try:
                kids_section.find_elements_by_css_selector(Constant.RADIO_LABEL)[0].click()
                break
            except:
                kids_section = self.browser.find_elements_by_css_selector(Constant.NOT_MADE_FOR_KIDS_LABEL)
                time.sleep(Constant.USER_WAITING_TIME)

        logger.debug('Selected \"{}\"'.format(Constant.NOT_MADE_FOR_KIDS_LABEL))

        playlist = self.video_playlist
        if playlist:
            self.browser.find_element(By.CLASS_NAME, Constant.PL_DROPDOWN_CLASS).click()
            time.sleep(Constant.USER_WAITING_TIME)
            search_field = self.browser.find_element(By.ID, Constant.PL_SEARCH_INPUT_ID)
            self.__write_in_field(search_field, playlist)
            time.sleep(Constant.USER_WAITING_TIME * 2)
            playlist_items_container = self.browser.find_element(By.ID, Constant.PL_ITEMS_CONTAINER_ID)
            logger.debug('Playlist xpath: "{}".'.format(Constant.PL_ITEM_CONTAINER.format(playlist)))
            playlist_item = playlist_items_container.find_element(By.XPATH, Constant.PL_ITEM_CONTAINER.format(playlist))
            if playlist_item:
                logger.debug('Playlist found.')
                playlist_item.click()
                time.sleep(Constant.USER_WAITING_TIME)
            else:
                logger.debug('Playlist not found. Creating')
                self.__clear_field(search_field)
                time.sleep(Constant.USER_WAITING_TIME)

                new_playlist_button = self.browser.find_element(By.CLASS_NAME, Constant.PL_NEW_BUTTON_CLASS)
                new_playlist_button.click()

                create_playlist_container = self.browser.find_element(By.ID, Constant.PL_CREATE_PLAYLIST_CONTAINER_ID)
                playlist_title_textbox = create_playlist_container.find_element(By.XPATH, "//textarea")
                self.__write_in_field(playlist_title_textbox, playlist)

                time.sleep(Constant.USER_WAITING_TIME)
                create_playlist_button = self.browser.find_element(By.CLASS_NAME, Constant.PL_CREATE_BUTTON_CLASS)
                create_playlist_button.click()
                time.sleep(Constant.USER_WAITING_TIME)

            done_button = self.browser.find_element(By.CLASS_NAME, Constant.PL_DONE_BUTTON_CLASS)
            done_button.click()

        try:
            self.browser.find_element_by_css_selector(Constant.ADVANCED_BUTTON_ID).click()
        except:
            logger.error('Could not find advanced button')
            return 'Fatal'
        logger.debug('Clicked MORE OPTIONS')
        time.sleep(Constant.USER_WAITING_TIME)

        tags = self.video_tags
        if tags:
            tags_container = self.browser.find_element_by_css_selector(Constant.TAGS_CONTAINER_ID)
            tags_field = tags_container.find_element_by_css_selector(Constant.TAGS_INPUT)
            self.__write_in_field(tags_field, ','.join(tags))
            logger.debug('The tags were set to \"{}\"'.format(tags))

        self.browser.find_element_by_css_selector(Constant.NEXT_BUTTON).click()
        logger.debug('Clicked {} one'.format(Constant.NEXT_BUTTON))

        self.browser.find_element_by_css_selector(Constant.NEXT_BUTTON).click()
        logger.debug('Clicked {} two'.format(Constant.NEXT_BUTTON))

        self.browser.find_element_by_css_selector(Constant.NEXT_BUTTON).click()
        logger.debug('Clicked {} three'.format(Constant.NEXT_BUTTON))
        public_main_button = self.browser.find_element_by_css_selector(Constant.PUBLIC_BUTTON)
        public_main_button.find_element_by_css_selector(Constant.RADIO_LABEL).click()
        logger.debug('Made the video {}'.format(Constant.PUBLIC_BUTTON))

        uploading_status_container = None
        while uploading_status_container is not None:
            try:
                uploading_status_container = self.browser.find_element_by_css_selector(
                    Constant.UPLOADING_STATUS_CONTAINER)
            except:
                continue
            uploading_progress = uploading_status_container.get_attribute('value')
            logger.debug('Upload video progress: {}%'.format(uploading_progress))
            time.sleep(Constant.USER_WAITING_TIME * 5)
            uploading_status_container = self.browser.find_element_by_css_selector(Constant.UPLOADING_STATUS_CONTAINER)

        logger.debug('Upload container gone.')

        done_button = self.browser.find_element_by_css_selector(Constant.DONE_BUTTON)

        if done_button.get_attribute('aria-disabled') == 'true':
            error_message = self.browser.find_element_by_css_selector(Constant.ERROR_CONTAINER).text
            logger.error(error_message)
            return 'Error'

        done_button.click()
        logger.debug(
            f"Publishing video {self.video_title}")
        time.sleep(Constant.USER_WAITING_TIME * 10)
        self.browser.get(Constant.YOUTUBE_URL)
        return 'Success'

    def __quit(self):
        self.browser.quit()

    def hide_element(self):
        self.browser.execute_script("""const callout = document.querySelector('[id="callout"]');
            if (callout) {
              callout.style.display = 'none';
            }""")

    def youtube_send_comment(self, video_url, comment_text):
        try:
            self.browser.get(video_url)
        except:
            logger.info('Не удалось открыть страницу видео')
            return False

        for x in range(7):
            try:
                comment_area = self.browser.find_element_by_css_selector('[id="placeholder-area"]')
                comment_area.click()
                break
            except:
                self.browser.find_element_by_tag_name('body').send_keys(Keys.HOME)
                for x in range(1):
                    self.browser.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN * 10)
                    time.sleep(1)

        else:
            logger.info('Не удалось найти поле для ввода комментария')
            return False

        pyperclip.copy(comment_text)
        # pyperclip.copy(random.choice(cite))
        try:
            self.browser.find_element_by_css_selector('[id="contenteditable-root"]').send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            self.browser.find_element_by_css_selector('[id="submit-button"]').click()
        except:
            logger.info('Не удалось отправить комментарий')
            return False
        time.sleep(10)
        return True

    def youtube_check_comment(self, video_url, text):
        try:
            self.browser.get(video_url)
        except:
            logger.info('Не удалось открыть страницу видео')
            return False

        for x in range(10):
            try:
                trigger = self.browser.find_element_by_css_selector('[id="trigger"]')
                trigger.click()
                break
            except:
                try:
                    self.browser.find_element_by_tag_name('body').send_keys(Keys.HOME)
                    for x in range(1):
                        self.browser.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN * 10)
                        time.sleep(1)
                except:
                    pass
                time.sleep(1)

        else:
            logger.info('Не удалось найти триггер')
            return False

        time.sleep(3)

        try:
            self.browser.find_element_by_css_selector('[class="yt-simple-endpoint style-scope yt-dropdown-menu"]').click()
        except:
            logger.info('Не удалось нажать на кнопку "Показать все комментарии"')
            return False

        for x in range(10):
            comments = self.browser.find_elements_by_css_selector('[id="content-text"]')
            if not comments:
                time.sleep(1)
                continue
            for comment in comments:
                try:
                    comment_text = comment.text
                except:
                    continue
                if text in comment_text:
                    return True

            time.sleep(1)
        else:
            logger.info('Не удалось найти комментарий')
            return False



class Constant:
    """A class for storing constants for YoutubeUploader class"""
    YOUTUBE_URL = 'https://www.youtube.com'
    YOUTUBE_STUDIO_URL = 'https://studio.youtube.com'
    YOUTUBE_UPLOAD_URL = 'https://www.youtube.com/upload'
    USER_WAITING_TIME = 1
    VIDEO_TITLE = 'title'
    VIDEO_DESCRIPTION = 'description'
    VIDEO_EDIT = 'edit'
    VIDEO_TAGS = 'tags'
    TEXTBOX_ID = '[id="textbox"]'
    TEXT_INPUT = 'text-input'
    RADIO_LABEL = '[id="radioLabel"]'
    UPLOADING_STATUS_CONTAINER = '[checks-summary-status-v2*="UPLOAD"]'
    NOT_MADE_FOR_KIDS_LABEL = '[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]'

    UPLOAD_DIALOG = '//ytcp-uploads-dialog'
    ADVANCED_BUTTON_ID = '[id="toggle-button"]'
    TAGS_CONTAINER_ID = '[id="tags-container"]'

    TAGS_INPUT = '[id="text-input"]'
    NEXT_BUTTON = '[id="next-button"]'
    PUBLIC_BUTTON = '[name="PUBLIC"]'
    VIDEO_URL_CONTAINER = "//span[@class='video-url-fadeable style-scope ytcp-video-info']"
    VIDEO_URL_ELEMENT = "//a[@class='style-scope ytcp-video-info']"
    HREF = 'href'
    ERROR_CONTAINER = '[id="error-message"]'
    VIDEO_NOT_FOUND_ERROR = 'Could not find video_id'
    DONE_BUTTON = '[id="done-button"]'
    INPUT_FILE_VIDEO = "[type='file']"
    INPUT_FILE_THUMBNAIL = "//input[@id='file-loader']"

    # Playlist
    VIDEO_PLAYLIST = 'playlist_title'
    PL_DROPDOWN_CLASS = 'ytcp-video-metadata-playlists'
    PL_SEARCH_INPUT_ID = 'search-input'
    PL_ITEMS_CONTAINER_ID = 'items'
    PL_ITEM_CONTAINER = '//span[text()="{}"]'
    PL_NEW_BUTTON_CLASS = 'new-playlist-button'
    PL_CREATE_PLAYLIST_CONTAINER_ID = 'create-playlist-form'
    PL_CREATE_BUTTON_CLASS = 'create-playlist-button'
    PL_DONE_BUTTON_CLASS = 'done-button'
