import os

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from riddles import util


class TestUnitIsSquare(TestCase):
    # Square numbers
    def test_0_is_square(self):
        self.assertTrue(util.is_square(0))

    def test_1_is_square(self):
        self.assertTrue(util.is_square(1))

    def test_4_is_square(self):
        self.assertTrue(util.is_square(4))

    def test_9_is_square(self):
        self.assertTrue(util.is_square(9))

    def test_81_is_square(self):
        self.assertTrue(util.is_square(81))

    # Non square numbers
    def test_2_is_not_square(self):
        self.assertFalse(util.is_square(2))

    def test_500_is_not_square(self):
        self.assertFalse(util.is_square(500))

    # Negative numbers
    def test_neg0_is_square(self):
        self.assertTrue(util.is_square(-0))

    def test_neg1_is_not_square(self):
        self.assertFalse(util.is_square(-1))

    def test_neg2_is_not_square(self):
        self.assertFalse(util.is_square(-2))

    def test_neg81_is_not_square(self):
        self.assertFalse(util.is_square(-81))

    def test_neg500_is_not_square(self):
        self.assertFalse(util.is_square(-500))


class TestSeleniumRiddle(LiveServerTestCase):
    def setUp(self):
        path = 'C:\\Users\\danie\\webdrivers\\marionette\\wires.exe'
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities['binary'] = path

        desired_cap = {
            'platform': "Mac OS X 10.9",
            'browserName': "chrome",
            'version': "31",
            'tunnel-identifier': os.environ["TRAVIS_JOB_NUMBER"],
        }
        executor = "http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(
            os.environ["SAUCE_USERNAME"],
            os.environ["SAUCE_ACCESS_KEY"],
        )
        self.selenium = webdriver.Remote(
            command_executor=executor,
            desired_capabilities=desired_cap,
        )

        super(LiveServerTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(LiveServerTestCase, self).tearDown()

    def test_riddle_exists(self):
        selenium = self.selenium
        selenium.get('ondemand.saucelabs.com:80/riddles/sudoku/1/')
        riddle = selenium.find_element_by_id('riddle')
        self.assertEqual(riddle.id, "riddle")
