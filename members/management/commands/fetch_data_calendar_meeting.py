from django.core.management.base import BaseCommand
from members.models import CalendarMeeting
import json #import module json

# def read_values_from_json(file, key):
#     values = []#create a list
#     with open(file) as f:# open a json file with my objects
#         data = json.load(f) # load all the data contained in this file f
#         for entry in data:# Create a new empty list
#             values.append(entry[key])# add each item in my list
#     return values # return my completed list 
CALENDAR = [
   "2021-01-05",
   "2021-01-06",
   "2021-01-07",
   "2021-01-12",
   "2021-01-13",
   "2021-01-14",
   "2021-01-19",
   "2021-01-20",
   "2021-01-21",
   "2021-01-26",
   "2021-01-27",
   "2021-01-28",
   "2021-02-02",
   "2021-02-03",
   "2021-02-04",
   "2021-02-09",
   "2021-02-11",
   "2021-02-16",
   "2021-02-17",
   "2021-02-18",
   "2021-03-09",
   "2021-03-10",
   "2021-03-11",
   "2021-03-16",
   "2021-03-17",
   "2021-03-18",
   "2021-03-23",
   "2021-03-24",
   "2021-03-25",
   "2021-03-30",
   "2021-03-31",
   "2021-04-01",
   "2021-04-06",
   "2021-04-07",
   "2021-04-08",
   "2021-04-13",
   "2021-04-14",
   "2021-04-15",
   "2021-04-20",
   "2021-04-21",
   "2021-04-22",
   "2021-05-11",
   "2021-05-12",
   "2021-05-18",
   "2021-05-19",
   "2021-05-20",
   "2021-05-25",
   "2021-05-26",
   "2021-05-27",
   "2021-06-01",
   "2021-06-02",
   "2021-06-03",
   "2021-06-08",
   "2021-06-09",
   "2021-06-10",
   "2021-06-15",
   "2021-06-16",
   "2021-06-17"
   ]

class Command(BaseCommand):
    
    help = 'Va permettre de remplir les tables(CalendarMeeting,...)\
            de notre base de données'

    def handle(self, *args, **options):
        """
        we load the different dates in table calendarmetting
        """
        # all_values = read_values_from_json("calendar.json","date")
        for date in CALENDAR:
            # We fill the data base members.calendarmetting
            CalendarMeeting.objects.update_or_create(
                date=date,                
                )
 