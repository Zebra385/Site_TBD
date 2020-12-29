from django.core.management.base import BaseCommand
from members.models import CalendarMeeting
import json #import module json


class Command(BaseCommand):
    
    help = 'Load tables(CalendarMeeting,...)\
            in our DataBase'

    def handle(self, *args, **options):
        """
        we load the different dates in table calendarmetting
        """
        
        def read_values_from_json(file):
            values = []#create a list
            with open(file) as f:# open a json file with my objects
                data = json.load(f) # load all the data contained in this file f
            for entry in data:# Create a new empty list
                
                values.append(entry)# add each item in my list
                
            return values # return my completed list 
        
        # read_values_from_json('calendar.json')
        all_values = read_values_from_json("calendar.json")
        for date in all_values:
            # We fill the data base members.calendarmetting
            CalendarMeeting.objects.update_or_create(
                date=date,                
                )