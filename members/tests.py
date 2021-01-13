from django.test import TestCase
from django.urls import reverse
from django.core import mail
from members.forms import ExchangeMeetingForm
from members.create_calendar import calendar, read_json
from members.create_calendar import calendar1, calendar_customuser
from members.models import CalendarMeeting, CalendarCustomuser
from members.models import ExchangeMeeting, ListExchangeMeeting, Meeting
from accounts.models import CustomUser
from members.views import AccueilMemberView
from members.views import CalendarExchangeMeeting


class AccueilMemberViewTestCase(TestCase):
    def setUp(self):
        """
        We create data in the  tables CalendarMeeting CalendarCustomuser
        and Customuser
        """
        all_values_customuser = read_json("customuser_demo.json")
        for val in all_values_customuser:
            # We fill the data base members.calendarmetting
            CustomUser.objects.create(
                password=val["fields"]["password"],
                username=val["fields"]["username"],
                email=val["fields"]["email"],
                )
        # we create a user connect
        self.user = CustomUser.objects.get(email='houche@orange.fr')
        all_values = read_json("calendar.json")
        for date in all_values:
            # We fill the data base members.calendarmetting
            CalendarMeeting.objects.create(
                date=date,
                )
        self.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        self.calendar = calendar(self.day_list)
        all_values_calendar_user = read_json("calendarcustomuser_demo.json")
        for date in all_values_calendar_user:
            auth_user = CustomUser.objects.get(pk=date["fields"]["auth_user"])
            date_meeting = CalendarMeeting.objects.get(
                pk=date["fields"]["date_meeting"])
            # We fill the data base members.calendarmetting
            CalendarCustomuser.objects.create(
                auth_user=auth_user,
                date_meeting=date_meeting,
                )

        self.day_list_customuser = list(
            CalendarCustomuser.objects.filter(
                auth_user=self.user
                ).order_by('date_meeting')
                )
        self.calendar_user = calendar1(self.day_list_customuser)
        self.calendar_customuser = calendar_customuser(
            self.calendar_user,
            self.calendar
            )

    def test_environment_set_in_context(self):
        """
        Test the context data
        """
        request = self.client.get(
            '/',
            data={'calendar': self.calendar,
                  'calendar_customuser': self.calendar_customuser, })
        request.user = self.user
        view = AccueilMemberView()
        view.setup(request)
        # we fix the object _list because we do not call
        # SearchProduct as a view
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertIn('calendar', context)
        self.assertIn('calendar_customuser', context)


class CallExchangeMeetingTestCase(TestCase):
    """
    This test to test a call of exchange meeting
    """
    fixtures = [
        'calendarmeeting_demo.json',
        'meeting_demo.json',
        'gang_demo.json',
        'customuser_demo.json',
        'calendarcustomuser_demo.json'
        ]

    def setUp(self):
        """
        We create data for this test
        """
        self.user = CustomUser.objects.get(username='HOUCHE')
        self.form_class = ExchangeMeetingForm
        self.groupe = Meeting.objects.get(day="Mercredi")

    def test_get_call(self):
        """
        Test the method get
        """
        response = self.client.login(
                                     username='houche@orange.fr',
                                     password='felixt12'
                                     )
        self.assertEqual(response, True)
        user = CustomUser.objects.get(username="HOUCHE")
        request = self.client.get(
            reverse('members:registercall'),
            data={"auth_user": user, })
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'members/register_call.html')

    def test_post_call(self):
        """
        Test the method post
        """

        response1 = self.client.login(
                                      username='houche@orange.fr',
                                      password='felixt12'
                                      )
        self.assertEqual(response1, True)
        user = CustomUser.objects.get(username="HOUCHE")
        response = self.client.post(
            reverse('members:registercall'),
            data={
                  "auth_user": user,
                  'call_meeting_0': 5,
                  'call_meeting_1': 1,
                  'call_meeting_2': 2021,
                  'groupe': 2,
                  'free_date1_0': 6,
                  'free_date1_1': 1,
                  'free_date1_2': 2021,
                  'free_date2_0': 13,
                  'free_date2_1': 1,
                  'free_date2_2': 2021,
                  'free_date3_0': 20,
                  'free_date3_1': 1,
                  'free_date3_2': 2021,
                })
        # code 302 because redirection to
        # the /members/ConfirmCallExchangeMeeting/
        # self.assertEqual(response.call_meeting,'2021-01-05')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/members/ConfirmCallExchangeMeeting/')

    def test_send_call_email(self):
        """
        We test if a email is send
        """
        # Send message.
        mail.send_mail(
            'Rendez-vous sur le site ',
            'Demande d\'échange de séance',
            'jacob@orange.fr', ['to@example.com'],
            fail_silently=False,
        )
        # time.sleep(2)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(
            mail.outbox[0].subject,
            'Rendez-vous sur le site ')


class CalendarExchangeMeetingTestCase(TestCase):
    """
    Test an accept exchange of meeting
    """
    fixtures = [
        'calendarmeeting_demo.json',
        'meeting_demo.json',
        'gang_demo.json',
        'customuser_demo.json',
        'calendarcustomuser_demo.json'
        ]

    def setUp(self):
        """
        Data for this test
        """

        self.user = CustomUser.objects.get(username='HOUCHE')
        # we need 2 meetings for ExchangeMeeting
        # the first for caller
        self.date1 = CalendarMeeting.objects.get(
                date="2021-01-05",
                )
        # the second  for date free for the caller
        self.date2 = CalendarMeeting.objects.get(
                date="2021-01-06",)
        # we create an exchange meeting
        ExchangeMeeting.objects.create(
                exchange_operational=False,
                caller=self.user,
                caller_meeting=self.date1
            )
        self.exchange_meeting = ExchangeMeeting.objects.get(
                exchange_operational=False)
        # We create group

        self.groupe = Meeting.objects.get(day="Mercredi")
        # we create an list exchange meeting
        ListExchangeMeeting.objects.create(
                exchange_meeting=self.exchange_meeting,
                date_meeting1=self.date2,
                date_meeting2=None,
                date_meeting3=None,
                groupe=self.groupe
                )
        self.list_exchange_meeting = ListExchangeMeeting.objects.get(
                exchange_meeting=self.exchange_meeting)
        self.form_class = ExchangeMeetingForm

    def test_environment_set_in_context(self):
        """
        Test the context data
        """
        request = self.client.get(
            '/',
            data={'listexchangemeeting': self.exchange_meeting, })
        request.user = self.user
        view = CalendarExchangeMeeting()
        view.setup(request)
        # we fix the object _list because we do not call
        # SearchProduct as a view
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertIn('listexchangemeeting', context)

    def test_post_confirm(self):
        """
        Test methode post
        """
        response1 = self.client.login(
                                      username='houche@gmail.com',
                                      password='felixt25'
                                      )
        self.assertEqual(response1, True)
        choice = self.list_exchange_meeting.id
        response = self.client.post(reverse('members:calendarexchangemeeting'),
                                    data={
                                        'choice': choice,
                                        'elements': 1,
                                        })
        # code 302 because redirection to
        # the /members/ConfirmAcceptExchangeMeeting/
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             '/members/ConfirmAcceptExchangeMeeting/'
                             )

    def test_send_confirm_email(self):
        """
        We test if a email is send
        """
        # Send message.
        mail.send_mail(
            'Confirmation échange',
            'Demande d\'échange de séance',
            'jacob@orange.fr', ['to@example.com'],
            fail_silently=False,
        )
        # time.sleep(2)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(
            mail.outbox[0].subject,
            'Confirmation échange')
