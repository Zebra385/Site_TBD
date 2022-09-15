from django.core.management.base import BaseCommand
from members.models import Gang, CalendarCustomuser, CalendarMeeting
from accounts.models import CustomUser
from members.create_calendar import day_list


class Command(BaseCommand):

    help = 'Load the table(CalendarCustomuser,...)\
            of our DataBase'

    def handle(self, *args, **options):
        """
        we load the calendar for each user
        """
        all_users = CustomUser.objects.all()
        self.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        self.tuesday_list = day_list(self.day_list, 1)
        self.wenesday_list = day_list(self.day_list, 2)
        self.thursday_list = day_list(self.day_list, 3)
        for user in all_users:
            meeting = []
            t = CustomUser.objects.get(pk=user.id).id
            number_per_gang = 12
            max_custumuser = 3 + (5 * number_per_gang)
            # t==1 for the administrator and t > max_custumuser for the teachers
            if t == 1 or t > max_custumuser:
                pass
            else:
                try:
                    gang_user = Gang.objects.get(auth_user=t)
                    number_gang = gang_user.meeting_id

                    # if the day is tuesday
                    if number_gang.day == "Mardi":
                        meeting = self.tuesday_list
                    # is  wenesday
                    if number_gang.day == "Mercredi":
                        meeting = self.wenesday_list
                    # is  thursday

                    if number_gang.day == "Jeudi":
                        meeting = self.thursday_list
                    for day in meeting:
                        id_meeting = CalendarMeeting.objects.get(date=day)
                        CalendarCustomuser.objects.update_or_create(
                            auth_user=CustomUser.objects.get(pk=t),
                            date_meeting=CalendarMeeting.objects.get(
                                pk=id_meeting.id
                                )
                        )
                except Gang.DoesNotExist:
                    pass

        # test
        # all_calendar_customuser = CalendarCustomuser.objects.filter(
        #     auth_user=12
        #     )
        # for m in all_calendar_customuser:
        #     print("numero ", m.id,
        #           " le nom est:", m.auth_user,
        #           'pour le cours du: ', m.date_meeting.date
                #   )
