from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser

class MylogoutTestcase(TestCase):

    def test_logout(self):
        self.client.logout()
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class RegistrationTestcase(TestCase):

    def test_form_valid(self):
        form = CustomUser(
                    username='jacob',
                    email= 'jacob@orange.fr',
                    password='Marmote§',
                    
        )
        
        
        self.assertEqual(form.username, 'jacob')
        self.assertEqual(form.email, 'jacob@orange.fr')

 

# class MyloginTestcase(TestCase):
    
#     def test_reset_password(self):
#         self.client.login()
#         response = self.client.post(reverse('accounts:reset_password'))
#         self.assertEqual(response.status_code, 200)