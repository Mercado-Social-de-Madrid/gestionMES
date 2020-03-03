from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.urls import reverse
from selenium import webdriver

from mes import settings


class BadgeRenderer(object):

    badge = None
    driver = None
    DRIVER = 'chromedriver'

    def __init__(self, badge):
        self.badge = badge

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def configure_webdriver(self):
        weboptions = webdriver.ChromeOptions()
        weboptions.add_argument('headless')
        self.driver = webdriver.Chrome(self.DRIVER, chrome_options=weboptions)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1200, 850)


    def update_balance_image(self, balance):

        if balance.is_exempt or not balance.done:
            print('{}: No balance or exempt. Passing...'.format(balance.entity.display_name))
            return

        url = settings.BASESITE_URL + reverse('balance:badge_render', kwargs={'pk': self.badge.pk}) + '?id=' + str(balance.entity.pk)
        self.driver.get(url)

        img_temp = NamedTemporaryFile()
        png = self.driver.get_screenshot_as_png()
        img_temp.write(png)
        img_temp.flush()

        balance.badge_image.save(f"{balance.year}_{balance.entity.pk}", File(img_temp))
        balance.save()

