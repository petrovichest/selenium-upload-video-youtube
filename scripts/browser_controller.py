import os
import time
import traceback
import zipfile

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class BrowserController:
    def __init__(self, **kwargs):
        log_pass = kwargs.get('log_pass')
        profile_name = kwargs.get('profile_name')
        if log_pass:
            self.profile_name = log_pass.split('@')[0]
            self.profile_copy_path = f'{os.getcwd()}/Profiles/{log_pass.split("@")[0]}'
            self.proxy = kwargs.get('log_pass').split(';')[1]

        elif profile_name:
            try:
                self.profile_name = kwargs.get('profile_name').split(';')[0].split("\\")[-1]
                self.profile_path = kwargs.get('profile_name').split(';')[0].replace(self.profile_name, '')

                bot_folder = f'bot {self.profile_name.split(" ")[1]}'
                self.profile_copy_path = f'{self.profile_path}/{bot_folder}'
                self.proxy = kwargs.get('profile_name').split(';')[1]
            except:
                traceback.print_exc()
                pass
        self.chromedriver_path = f'{os.getcwd()}/chromedriver.exe'


    def start_browser(self, proxy=True, headless=False):


        print(f'Starting browser - {self.profile_name}')
        chrome_options = Options()

        if proxy:
            proxy = self.proxy
            if proxy:
            # self.proxy_list = self.get_proxy_from_file()
            # if self.proxy_list:
            #     proxy = random.choice(self.proxy_list)
                if '@' in proxy:
                    # pass
                    chrome_options.add_extension(self.proxy_with_password(proxy))
                else:
                    proxy_ip = proxy.split(':')[0]
                    proxy_port = proxy.split(':')[1]

                    chrome_options.add_argument('--proxy-server=' + proxy_ip + ':' + proxy_port)

        # chrome_options.add_extension('chrome_extensions\\fingerprint.crx')
        # chrome_options.add_extension('chrome_extensions\\font.crx')
        # chrome_options.add_extension('chrome_extensions\\webgl.crx')
        # chrome_options.add_extension('chrome_extensions\\random_useragent.crx')
        # chrome_options.add_argument('--ignore-certificate-errors')
        if headless == None or headless:
            chrome_options.add_argument('--headless')
            pass
        # chrome_options.add_argument(f'user-data-dir={self.profile_path}')

        try:
            os.mkdir(f'{os.getcwd()}/chromedrivers')
        except:
            pass

        chrome_options.add_argument(f"user-data-dir={self.profile_copy_path}")  # Path to your chrome profile
        chrome_options.add_argument(f'--profile-directory={self.profile_name}')
        # chrome_options.add_extension(f'./res/extensions/adblock.crx')
        # chrome_options.add_argument(f'--disable-dev-shm-usage')

        try:
            driver = webdriver.Chrome(self.chromedriver_path, chrome_options=chrome_options)
        except:
            traceback.print_exc()
            return False

        driver.set_window_size(1920, 1080)
        # self.driver.get('https://2ip.ru/')
        print('Browser started, proxy:', proxy)
        # if proxy:
        #     if not self.check_proxy(driver):
        #         return False
        return driver


    def get_proxy_from_file(self):
        try:
            with open(f'{os.getcwd()}/res/proxy.txt') as f:
                proxy_list = [x.strip() for x in f.read().split('\n') if x]
            return proxy_list
        except:
            return False

    def proxy_with_password(self, proxy):
        '91.107.119.216:65233@login:password'
        PROXY_HOST = proxy.split(':')[0]
        PROXY_PORT = proxy.split(':')[1].split('@')[0]
        PROXY_USER = proxy.split(':')[1].split('@')[1]
        PROXY_PASS = proxy.split(':')[2]

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        path = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        try:
            os.mkdir('proxy')
        except:
            pass
        pluginfile = f'proxy/proxy_auth_plugin_{self.profile_name}.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
        return pluginfile

    def browser_cache_clear(self, driver):
        # def expand_shadow_element(element):
        #     shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
        #     return shadow_root

        def checkbox_check(element):
            try:
                driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)['checked']
            except:
                return False
            return True
        try:
            driver.get('chrome://settings/clearBrowserData')
        except:
            return False
        for xdsgdsd in range(10):
            try:
                clear_window = driver.execute_script(
                    "return document.querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section > settings-privacy-page').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataDialog')")
                break
            except:
                time.sleep(1)
                continue
        else:
            return False
        try:
            browsingCheckboxBasic = clear_window.find_element_by_css_selector('[id="browsingCheckboxBasic"]')
            cookiesCheckboxBasic = clear_window.find_element_by_css_selector('[id="cookiesCheckboxBasic"]')
            cacheCheckboxBasic = clear_window.find_element_by_css_selector('[id="cacheCheckboxBasic"]')

            if not checkbox_check(browsingCheckboxBasic):
                browsingCheckboxBasic.click()
            if checkbox_check(cookiesCheckboxBasic):
                cookiesCheckboxBasic.click()
            if not checkbox_check(cacheCheckboxBasic):
                cacheCheckboxBasic.click()
            time_dropdown = clear_window.find_element_by_css_selector('[id="clearFromBasic"]')
            time_dropdown.click()
            time_dropdown.send_keys(Keys.ARROW_DOWN*4)
            time.sleep(1)
            confirm_button = clear_window.find_element_by_css_selector('[id="clearBrowsingDataConfirm"]')
            confirm_button.click()
        except:
            traceback.print_exc()
            return False
        for xdsgdsd in range(100):
            try:
                clear_window = driver.execute_script(
                    "return document.querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section > settings-privacy-page').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataDialog')")
                time.sleep(1)
                continue
            except:
                break
        return True

    def close_all_windows(self, driver):
        # driver = webdriver.Firefox(firefox_profile=fp, options=options)

        while True:
            try:
                active_windows = driver.window_handles
            except:
                return True

            try:
                if active_windows:
                    driver.switch_to_window(active_windows[-1])
                    driver.close()
                    driver.switch_to_window(active_windows[0])
                    continue
                else:
                    return True
            except:
                pass

    def close_all_unnecessary_windows(self, driver):
        trusted_urls = ['all-access.wax.io', 'play.pocketaliens.io']
        while True:
            try:
                active_windows = driver.window_handles
            except:
                return True
            for one_active_window in driver.window_handles:

                for xffsdfsd in range(10):
                    try:
                        driver.switch_to_window(one_active_window)
                        driver_current_url = driver.current_url
                        window_url = driver_current_url.split('/')[2]
                        break
                    except:
                        traceback.print_exc()
                        time.sleep(1)
                else:
                    return False

                for one_trusted_url in trusted_urls:
                    if one_trusted_url in window_url:
                        break
                else:
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
                    break

            else:
                driver.switch_to_window(driver.window_handles[0])
                return True

    def close_all_windows_without_first(self, driver):
        while True:
            all_opened_windows = driver.window_handles
            if len(all_opened_windows) > 1:
                for one_opened_window in all_opened_windows[1:]:
                    try:
                        driver.switch_to_window(one_opened_window)
                        driver.close()
                        driver.switch_to_window(all_opened_windows[0])
                    except:
                        continue
            else:
                driver.switch_to_window(all_opened_windows[0])
                return True


if __name__ == '__main__':
    driver = BrowserController(profile_name=r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\bot35\profile 35;91.229.79.73:45785@Selandreyslizh1:O7p5TdK').start_browser(proxy=True, headless=False)
    input('sdgsdgs')