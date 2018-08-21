import os
import unittest

from django.conf import settings
from django.test import LiveServerTestCase
from selenium.webdriver import Firefox, Remote
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait


@unittest.skipUnless(settings.SELENIUM is True or 'CI' in os.environ,
                     'Selenium test cases are only run in CI or if configured explicitly.')
class SeleniumTestCase(LiveServerTestCase):

    def setUp(self):
        if 'CI' in os.environ:
            self.driver = self.sauce_chrome_webdriver()
        elif settings.SELENIUM is True:
            options = FirefoxOptions()
            options.add_argument('-headless')
            self.driver = Firefox(firefox_options=options)
        self.driver.implicitly_wait(10)

    def sauce_chrome_webdriver(self):
        class_name = self.__class__.__name__
        method_name = self._testMethodName
        tunnel_id = os.environ.get("TRAVIS_JOB_NUMBER")
        capabilities = {
            'platform': "Mac OS X 10.9",
            'browserName': "chrome",
            'version': "31",
            'name': '{}.{}'.format(class_name, method_name),
            'tunnel-identifier': tunnel_id,
        }

        executor = "http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(
            os.environ["SAUCE_USERNAME"],
            os.environ["SAUCE_ACCESS_KEY"],
        )
        return Remote(
            command_executor=executor,
            desired_capabilities=capabilities,
        )

    def tearDown(self):
        WebDriverWait(self.driver, 10)
        self.driver.quit()
