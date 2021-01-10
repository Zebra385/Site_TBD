from django.test import TestCase, RequestFactory
from django.urls import reverse
from members.create_calendar import calendar, read_json
from members.models import CalendarMeeting
from .views import AccueilView

class AccueilPageTestCase(TestCase):
    """
    Test that accueil page returns a 200 if the item exists.
    """
    def test_accueil_page(self):
        response = self.client.get(reverse('workshop:accueil'))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        """
        We create data in the  table CalendarMeeting
        """
        all_values = read_json("calendar.json")
        for date in all_values:
            # We fill the data base members.calendarmetting
            CalendarMeeting.objects.create(
                date=date,
                )
        self.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        self.calendar = calendar(self.day_list)  

    def test_environment_set_in_context(self):
        """
        Test the context data
        """
        request = self.client.get('/', data={'calendar': self.calendar})
        view = AccueilView()
        view.setup(request)
        # we fix the object _list because we do not call
        # SearchProduct as a view
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertIn('calendar', context)


class CoursViewTestCase(TestCase):
    """
    Test that cours page returns a 200 if the item exists.
    """
    def test_cours_page(self):
        response = self.client.get(reverse('workshop:cours'))
        self.assertEqual(response.status_code, 200)


class StagesViewTestCase(TestCase):
    """
    Test that stage page returns a 200 if the item exists.
    """
    def test_stages_page(self):
        response = self.client.get(reverse('workshop:stages'))
        self.assertEqual(response.status_code, 200)
