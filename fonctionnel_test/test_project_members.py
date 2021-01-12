from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from accounts.models import CustomUser
from members.models import CalendarMeeting, Meeting
import time
from members.create_calendar import calendar, read_json


class TestCallExchangeMeeting(StaticLiveServerTestCase):
    """
    Test fonctionnal to test if the user cans call an exchange meeting
    First login first user
    Go to the page to  create an exchange meeting
    Logout
    Second login second user
    Go to the page to accept the previous exchange meeting
    """
    @classmethod
    def setUpClass(cls):
        # it is to declare what we need in this test
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

        all_values_customuser = read_json("customuser.json")
        for val in all_values_customuser:
            # We fill the data base customuser
            CustomUser.objects.create(
                password=val["fields"]["password"],
                username=val["fields"]["username"],
                email=val["fields"]["email"],
                )

        # we create a user connect
        cls.user = CustomUser.objects.get(email='houche.serge@orange.fr')
        all_values = read_json("calendar.json")
        for date in all_values:
            # We fill the data base members.calendarmetting
            CalendarMeeting.objects.create(
                date=date,
                )

        cls.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        cls.calendar = calendar(cls.day_list)
        cls.all_values_calendar_user = read_json("calendarcustomuser.json")
        # we create a group for an exchange
        Meeting.objects.create(
                day="Mercredi",
                time_slot="19h30-22h00",
                time=2.5,
                )
        cls.groupe = Meeting.objects.get(day="Mercredi")

    @classmethod
    def tearDownClass(cls):
        # to find the test , we quit the webdriver
        cls.selenium.quit()
        super().tearDownClass()

    def test_call_exchange_selenium(self):
        # We open the page in localhost server to login
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/accounts/login/')
            )

        self.assertIn("Se connecter", self.selenium.title)
        time.sleep(2)
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('houche.serge@orange.fr')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('felixt12')

        time.sleep(2)
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(2)
        # we go in the page registerCall to call an exchangemeeting
        self.selenium.get(
                    '%s%s' % (self.live_server_url, '/members/RegisterCall/'))
        page_url = self.selenium.current_url
        self.assertEqual(page_url,
                         '%s%s' % (self.live_server_url,
                                   '/members/RegisterCall/'
                                   ))
        self.assertIn("Demande d'échange de séance", self.selenium.title)
        time.sleep(2)
        # we fill the form
        call_meeting_0_input = self.selenium.find_element_by_name(
            "call_meeting_0")
        call_meeting_0_input.send_keys(5)
        call_meeting_1_input = self.selenium.find_element_by_name(
            "call_meeting_1")
        call_meeting_1_input.send_keys(0)
        call_meeting_2_input = self.selenium.find_element_by_name(
            "call_meeting_2")
        call_meeting_2_input.send_keys(2021)

        groupe_input = self.selenium.find_element_by_name("groupe")
        groupe_input.send_keys(str(self.groupe))

        free_date1_0_input = self.selenium.find_element_by_name("free_date1_0")
        free_date1_0_input.send_keys(6)
        free_date1_1_input = self.selenium.find_element_by_name("free_date1_1")
        free_date1_1_input.send_keys(0)
        free_date1_2_input = self.selenium.find_element_by_name("free_date1_2")
        free_date1_2_input.send_keys(2021)

        free_date2_0_input = self.selenium.find_element_by_name("free_date2_0")
        free_date2_0_input.send_keys(13)
        free_date2_1_input = self.selenium.find_element_by_name("free_date2_1")
        free_date2_1_input.send_keys(0)
        free_date2_2_input = self.selenium.find_element_by_name("free_date2_2")
        free_date2_2_input.send_keys(2021)

        free_date3_0_input = self.selenium.find_element_by_name("free_date3_0")
        free_date3_0_input.send_keys(20)
        free_date3_1_input = self.selenium.find_element_by_name("free_date3_1")
        free_date3_1_input.send_keys(0)
        free_date3_2_input = self.selenium.find_element_by_name("free_date3_2")
        free_date3_2_input.send_keys(2021)
        time.sleep(2)
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(2)
        # we logout to test the caledarexchangemeeting
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/accounts/logout/')
            )
        time.sleep(3)
        # We open a new page  in localhost server to login
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/accounts/login/')
            )
        time.sleep(3)
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('houche.serge@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('felixt25')
        time.sleep(3)
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(3)
        # We go to the page CalendarexchangeMeeting to accept an exchange
        self.selenium.get('%s%s' % (self.live_server_url,
                                    '/members/CalendarExchangeMeeting/'))
        page_url = self.selenium.current_url
        time.sleep(5)
        self.assertEqual(page_url, '%s%s' %
            (self.live_server_url, '/members/CalendarExchangeMeeting/'))
        self.assertIn("les demandes d'échanges de séances en cours",
                      self.selenium.title)
        time.sleep(5)
        self.selenium.find_element_by_xpath(
            '//input[@type="checkbox"][@value="1"]'
            ).click()
        time.sleep(3)
        # self.selenium.find_element_by_xpath('//input[@type="hidden"][@id="choice1"]')
        # time.sleep( 3 )
        self.selenium.find_element_by_xpath(
            '//button[@type="submit"][@value="Accepter cette échange"]'
            ).click()
        time.sleep(3)
