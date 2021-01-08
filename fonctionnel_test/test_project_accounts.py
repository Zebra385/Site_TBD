from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from accounts.models import CustomUser
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import time


class Registration(StaticLiveServerTestCase):
    """
    Test fonctionnal to test if the new user cans be create
    """
    @classmethod
    def setUpClass(cls):
        # it is to declare what we need in this test
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # to find the test , we quit the webdriver
        cls.selenium.quit()
        super().tearDownClass()

    def test_register_selenium(self):

        # We open the page in localhost server to reset our password
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/accounts/register/')
            )
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('jacob')
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('jacob@orange.fr')
        password1_input = self.selenium.find_element_by_name("password1")
        password1_input.send_keys('Marmote§')
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys('Marmote§')
        time.sleep(3)
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        time.sleep(3)
        self.selenium.get(
                    '%s%s' % (self.live_server_url, '/members/RegisterCall/'))


class TestResetPassword(StaticLiveServerTestCase):
    """
    Test fonctionnal to test if the user cans change
    his password
    """
    @classmethod
    def setUpClass(cls):
        # it is to declare what we need in this test
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)
        cls.user = CustomUser(
                    username='jacob',
                    email='jacob@orange.fr',
                    password='Marmote§',
        )
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        # to find the test , we quit the webdriver
        cls.selenium.quit()
        super().tearDownClass()

    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Réinitialisation du mot de passe',
            'Pour reinitialiser le message taper sur le lien: https://lien',
            'jacob@orange.fr', ['to@example.com'],
            fail_silently=False,
        )
        time.sleep(2)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(
            mail.outbox[0].subject,
            'Réinitialisation du mot de passe')

    def test_reset_password_selenium(self):

        # We open the page in localhost server to reset our password
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/accounts/reset_password/')
            )
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('jacob@orange.fr')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        time.sleep(2)

        # when we have receve a message, we click on a link
        # to can enter a new spassword
        # we need variables uid  and token whose send by the link
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        # We  ge to the page
        # {self.live_server_url}/accounts/reset/{uid}/{token}/
        # f behind is to convert the variable on  a string
        self.selenium.get(
            f"{self.live_server_url}/accounts/reset/{uid}/{token}/"
            )
        password1_input = self.selenium.find_element_by_name("new_password1")
        password2_input = self.selenium.find_element_by_name("new_password2")
        # we enter the new password
        password1_input.send_keys('elephant!')
        password2_input.send_keys('elephant!')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        time.sleep(2)