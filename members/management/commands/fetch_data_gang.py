from django.core.management.base import BaseCommand
from members.models import Meeting, Gang
from accounts.models import CustomUser

class Command(BaseCommand):
    
    help = 'Va permettre de remplir la table(gang,...)\
            de notre base de données'

    def handle(self, *args, **options):
        """
        we load the different gang in table gang
        """
        all_users=CustomUser.objects.all()
        # gang=1 tuesday afternoon, 
        # gang=2 tuesday evening,
        # gang=3 wenesday evening,
        # gang=4 thursday morning,
        # gang=5 thursday afternoon,
        for number_gang in range(0,5):
            begin = int(3 + number_gang*9)
            end =  int(12 + number_gang*9)
            for number_id in range(begin, end):
                # We fill the data base members.meeting
                # user = CustomUser.objects.get(pk=number_id)
                # id_user = user.id
                auth_user = CustomUser.objects.get(pk=number_id)
                meeting_id=Meeting.objects.get(pk=number_gang+1)
                print(" le numero du nom est:",auth_user.id,'pour le cours numero ',meeting_id.id)
                Gang.objects.update_or_create(
                    auth_user=auth_user.id,
                    meeting_id=meeting_id.id,
                   
                    )
        # test
        all_gang=Gang.objects.all()
        for m in all_gang:
            print("numero ", m.id," le nom est:",m.auth_user,'pour le cours du: ',m.meeting_id.day)
 