import os

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SeleniumTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = self.sauce_chrome_webdriver()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()

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
        return webdriver.Remote(
            command_executor=executor,
            desired_capabilities=capabilities,
        )

    def local_chrome_webdriver(self):
        return webdriver.Chrome("webdrivers/windows/chromedriver.exe")

    def local_firefox_webdriver(self):
        caps = DesiredCapabilities.FIREFOX
        # caps['marionette'] = True
        caps['binary'] = "webdrivers/windows/wires.exe"
        return webdriver.Firefox(capabilities=caps)
