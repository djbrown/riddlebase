import os

from django.test import LiveServerTestCase
from selenium import webdriver


class SeleniumTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = self.sauce_web_driver()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        sauce_job_id = self.driver.session_id
        print("https://saucelabs.com/jobs/" + sauce_job_id)
        self.driver.quit()

    def sauce_web_driver(self):
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
