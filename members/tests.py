from django.test import TestCase
from members.create_calendar import calendar, read_json
from members.create_calendar import calendar1, calendar_customuser
from members.models import CalendarMeeting, CalendarCustomuser
from members.models import ExchangeMeeting, ListExchangeMeeting, Meeting
from accounts.models import CustomUser
from members.views import AccueilMemberView, CalendarExchangeMeeting


class AccueilMemberViewTestCase(TestCase):
    def setUp(self):
        """
        We create data in the  tables CalendarMeeting CalendarCustomuser
        and Customuser
        """
        all_values_customuser = read_json("customuser.json")
        for val in all_values_customuser:
            # We fill the data base members.calendarmetting
            CustomUser.objects.create(
                password=val["fields"]["password"],
                username=val["fields"]["username"],
                email=val["fields"]["email"],
                )
        # we create a user connect
        self.user = CustomUser.objects.get(email='houche.serge@orange.fr')
        all_values = read_json("calendar.json")
        for date in all_values:
            # We fill the data base members.calendarmetting
            CalendarMeeting.objects.create(
                date=date,
                )
        self.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        self.calendar = calendar(self.day_list)
        all_values_calendar_user = read_json("calendarcustomuser.json")
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


class CalendarExchangeMeetingTestCase(TestCase):

    def setUp(self):
        """
        We create data in the  tables CalendarMeeting CalendarCustomuser
        and Customuser
        """
        CustomUser.objects.create(username='jacob',
                                  email='jacob@orange.fr',
                                  password='top_secret'
                                  )
        CustomUser.objects.create(username='adrien',
                                  email='adrien@orange.fr',
                                  password='secret_top'
                                  )
        self.user = CustomUser.objects.get(username='adrien')
        # we need 2 meetings for ExchangeMeeting
        # the first for caller
        CalendarMeeting.objects.create(
                date="2021-01-05",
                )
        self.date1 = CalendarMeeting.objects.get(
                date="2021-01-05",
                )
        # the second  for date free for the caller
        CalendarMeeting.objects.create(
                date="2021-01-06",
                )
        self.date2 = CalendarMeeting.objects.get(
                date="2021-01-06",)
        # we create an exchange meeting
        ExchangeMeeting.objects.create(
                exchange_operational=False,
                caller=self.user,
                caller_meeting=self.date1
            )
        self.exchange_meeting = ExchangeMeeting.objects.create(
                exchange_operational=False)
        # We create group

        Meeting.objects.create(
                day="Mercredi",
                time_slot="19h30-22h00",
                time=2.5,
                )
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

    def test_environment_set_in_context(self):
        """
        Test the context data
        """
        request = self.client.get(
            '/',
            data={'listexchangemeeting': self.list_exchange_meeting, })
        request.user = self.user
        view = CalendarExchangeMeeting()
        view.setup(request)
        # we fix the object _list because we do not call
        # SearchProduct as a view
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertIn('listexchangemeeting', context)
