import os
import sys
from unittest import skip

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
        capabilities = {
            'platform': "Mac OS X 10.9",
            'browserName': "chrome",
            'version': "31",
        }
        if os.environ.get("TRAVIS"):
            sys.stdout.write(os.environ["TRAVIS_JOB_NUMBER"])
            travis_job_number = os.environ["TRAVIS_JOB_NUMBER"][0]
            capabilities['tunnel-identifier'] = travis_job_number,

        executor = "http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(
            os.environ["SAUCE_USERNAME"],
            os.environ["SAUCE_ACCESS_KEY"],
        )
        self.selenium = webdriver.Remote(
            command_executor=executor,
            desired_capabilities=capabilities,
        )

        super(LiveServerTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(LiveServerTestCase, self).tearDown()

    def test_navbar_exists(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        sys.stdout.write(selenium.page_source)
        # navbar = selenium.find_element_by_id('navbar')
        # self.assertIsNotNone(navbar)

    @skip("Register page not implemented yet")
    def test_register(self):
        selenium = self.selenium

        # Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/accounts/register/')

        # find the form element
        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        submit = selenium.find_element_by_name('register')

        # Fill the form with data
        first_name.send_keys('Homer')
        last_name.send_keys('Simpson')
        username.send_keys('duffman')
        email.send_keys('homer@simpson.com')
        password1.send_keys('123456')
        password2.send_keys('123456')

        # submitting the form
        submit.send_keys(Keys.RETURN)

        # check the returned result
        assert 'Check your email' in selenium.page_source
