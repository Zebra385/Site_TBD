"""
file to test apps accounts
"""
import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from accounts.models import CustomUser



# class Registration(StaticLiveServerTestCase):
#     """
#     Test fonctionnal to test if the new user cans be create
#     """
#     @classmethod
#     def setUpClass(cls):
#         # it is to declare what we need in this test
#         super().setUpClass()
#         cls.selenium = webdriver.chrome()
#         cls.selenium.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         # to find the test , we quit the webdriver
#         cls.selenium.quit()
#         super().tearDownClass()

#     def test_register_selenium(self):
#         """
#         Test to know if we can register a new member
#         """
#         self.selenium.get(
#             '%s%s' % (self.live_server_url, '/')
#             )
#         page_url = self.selenium.current_url
#         self.assertEqual(page_url,
#                          '%s%s' % (self.live_server_url,
#                                    '/'
#                                    ))
#         page_url = self.selenium.current_url
#         self.assertEqual(page_url,
#                          '%s%s' % (self.live_server_url,
#                                    '/'
#                                    ))
#         self.assertIn("Atelier- Terre au Bout des Doigts", self.selenium.title)                           
#         # We open the page in localhost server to reset our password
#         wait = WebDriverWait(self.selenium, 10)   
#         self.selenium.get(
#             '%s%s' % (self.live_server_url, '/accounts/register/')
#             )
#         page_url = self.selenium.current_url
#         self.assertEqual(page_url,
#                          '%s%s' % (self.live_server_url,
#                                    '/accounts/register/'
#                                    ))
#         wait.until(EC.presence_of_element_located((By.NAME,'username')))
#         username_input = self.selenium.find_element_by_name("username")
#         username_input.send_keys('jacob')
#         email_input = self.selenium.find_element_by_name("email")
#         email_input.send_keys('jacob@orange.fr')
#         password1_input = self.selenium.find_element_by_name("password1")
#         password1_input.send_keys('Marmote§')
#         password2_input = self.selenium.find_element_by_name("password2")
#         password2_input.send_keys('Marmote§')
#         # time.sleep(3)
#         wait.until(EC.element_to_be_clickable((By.XPATH,'//input[@type="submit"]')))
#         self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
#         # time.sleep(3)
#         self.selenium.get(
#                     '%s%s' % (self.live_server_url, '/members/RegisterCall/'))


class TestResetPassword(StaticLiveServerTestCase):
    """
    Test fonctionnal to test if the user cans change
    his password
    """
    @classmethod
    def setUpClass(cls):
        # it is to declare what we need in this test
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
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
        """
        We test if a email is send
        """
        # Send message.
        mail.send_mail(
            'Réinitialisation du mot de passe',
            'Pour reinitialiser le message taper sur le lien: https://lien',
            'jacob@orange.fr', ['to@example.com'],
            fail_silently=False,
        )
        # time.sleep(2)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(
            mail.outbox[0].subject,
            'Réinitialisation du mot de passe')

    def test_reset_password_selenium(self):
        """
        we test if we can reset the password
        """
        # We open the page in localhost server to reset our password
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/accounts/reset_password/')
            )
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('jacob@orange.fr')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # time.sleep(2)

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
        # time.sleep(2)
