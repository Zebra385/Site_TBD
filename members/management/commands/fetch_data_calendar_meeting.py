from django.core.management.base import BaseCommand
from members.models import CalendarMeeting
from members.create_calendar import read_json



class Command(BaseCommand):

    help = 'Load tables(CalendarMeeting,...)\
            in our DataBase'

    def handle(self, *args, **options):
        """
        we load the different dates in table calendarmetting
        """

        # def read_values_from_json(file):
        #     # create a list
        #     values = []
        #     # open a json file with my objects
        #     with open(file) as f:
        #         # load all the data contained in this file f
        #         data = json.load(f)
        #     # Create a new empty list
        #     for entry in data:
        #         # add each item in my list
        #         values.append(entry)
        #     # return my completed list
        #     return values
        # # read_values_from_json('calendar.json')
        all_values = read_json("calendar.json")
        for date in all_values:
            # We fill the data base members.calendarmetting
            CalendarMeeting.objects.update_or_create(
                date=date,
                )
            print('date:',date)
