import time
import unittest

from django.contrib.auth.models import User
from django.core import mail
from selenium.webdriver.remote.webelement import WebElement

from base.tests.base import SeleniumTestCase


@unittest.skip
class TestPasswordChange(SeleniumTestCase):
    def test(self):
        self.assertEqual(mail.outbox, [])

        username = 'john'
        usermail = 'lennon@thebeatles.com'
        userpass = 'johnpassword'
        User.objects.create_user(username, usermail, userpass)

        self.navigate('users:login')
        reset_link: WebElement = self.driver.find_element_by_id('link-password-reset')
        reset_link.click()

        mail_textfield = self.driver.find_element_by_name('email')
        mail_textfield.send_keys(usermail)
        mail_textfield.submit()

        time.sleep(0.1)

        self.assertEqual(len(mail.outbox), 1)

        message: mail.EmailMessage = mail.outbox[0]
        self.assertEqual(message.to, [usermail])
        reactivation_link = message.body.splitlines()[5]
        self.assert_view_url('users:password_reset_change', url=reactivation_link)

        newpass = 'newpassword'
        self.driver.find_element_by_name('new_password1').send_keys(newpass)
        pass_textfield = self.driver.find_element_by_name('new_password2').send_keys(newpass)
        pass_textfield.submit()

        self.assert_view_url('users:password_reset_success')
