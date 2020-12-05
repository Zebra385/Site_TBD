from django.core.management.base import BaseCommand
from members.models import Meeting, DICTIONNARY_MEETING


class Command(BaseCommand):
    
    help = 'Va permettre de remplir les tables(Meeting,...)\
            de notre base de données'

    def handle(self, *args, **options):
        """
        we load the different days in table metting
        """
        for day in DICTIONNARY_MEETING:
            # We fill the data base members.meeting
            Meeting.objects.update_or_create(
                day=day[0],
                time_slot=day[1],
                time=day[2],
                )
 