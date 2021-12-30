import time


class TiktokController():

    def close_captcha(self, driver):

        for fsfsdf in range(10):
            try:
                driver.find_element_by_css_selector('[class="verify-bar-close--icon"]').click()
                return True
            except:
                time.sleep(1)
        else:
            return True

    def load_more(self, driver):
        for fsfsdf in range(10):
            try:
                driver.find_element_by_css_selector('[data-e2e="search-load-more"]').click()
                time.sleep(1)
                return True
            except:
                time.sleep(1)
        else:
            return True