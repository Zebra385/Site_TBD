from django.core.management.base import BaseCommand
from members.models import Meeting, Gang
from accounts.models import CustomUser
import time

class Command(BaseCommand):

    help = 'Load the table(Gang)\
            of our Database'

    def handle(self, *args, **options):
        """
        we load the different gang in table gang
        """
        # gang=1 tuesday afternoon,
        # gang=2 tuesday evening,
        # gang=3 wenesday evening,
        # gang=4 thursday morning,
        # gang=5 thursday afternoon,
        for number_gang in range(0, 5):
            begin = int(3 + number_gang*9)
            end = int(12 + number_gang*9)
            for number_id in range(begin, end):
                # We fill the table Customuser
                auth_user = CustomUser.objects.get(pk=number_id)
                meeting_id = Meeting.objects.get(pk=number_gang+1)
                Gang.objects.update_or_create(
                    auth_user=auth_user,
                    meeting_id=meeting_id,
                    )
        # test
        # all_gang=Gang.objects.all()
        # for m in all_gang:
        #     print("numero ", m.id," le nom est:",
        #            m.auth_user,'pour le cours du: ',
        #            m.meeting_id.day
        #           )
