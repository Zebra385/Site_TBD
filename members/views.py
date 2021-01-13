from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from members.models import CalendarCustomuser, CalendarMeeting
from accounts.models import CustomUser
from members.models import ExchangeMeeting, ListExchangeMeeting, Meeting, Gang
from datetime import date
from members.forms import ExchangeMeetingForm
from django.shortcuts import redirect
from django.core.mail import send_mail
from members.create_calendar import calendar, calendar_customuser
from members.create_calendar import calendar1, date_french
import datetime


@method_decorator(login_required(login_url='login'),
                  name='dispatch')
class AccueilMemberView(ListView):
    """ That class to get the acceuil page"""
    template_name = "members/accueil_member.html"
    context_object_name = 'calendar_meeting_list'
    model = CalendarCustomuser
    form = ExchangeMeetingForm

    def get_queryset(self):
        self.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        self.calendar = calendar(self.day_list)
        # test
        # for day in self.calendar:
        #     print('date calendar :', day)
        # load id for the user connect
        auth_user_id = self.request.user
        # load the calendar of this user
        self.day_list_customuser = list(
            CalendarCustomuser.objects.filter(
                auth_user=auth_user_id
                ).order_by('date_meeting')
                )
        self.calendar_user = calendar1(self.day_list_customuser)
        # test
        # for day in self.calendar_user:
        #     print('date calendar_user :', day)
        self.calendar_customuser = calendar_customuser(
            self.calendar_user,
            self.calendar
            )

        return self.calendar, self.calendar_customuser

    def get_context_data(self, **kwargs):
        kwargs['calendar'] = self.calendar
        kwargs['calendar_customuser'] = self.calendar_customuser
        return super(AccueilMemberView, self).get_context_data(**kwargs)


@method_decorator(login_required(login_url='login'),
                  name='dispatch')
class CallExchangeMeeting(View):
    """
    that class to show a form to call an exchange meeting
    """
    form_class = ExchangeMeetingForm
    template_name = 'members/register_call.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        auth_user = CustomUser.objects.get(pk=user.id)
        form = self.form_class(initial={'auth_user': auth_user, })
        context = {'form': form, }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            auth_user = self.request.user
            # auth_user=CustomUser.objects.get(pk=user.id)
            call_meeting = form.cleaned_data['call_meeting']
            call_meeting = CalendarMeeting.objects.get(date=call_meeting)
            # auth_user = form.cleaned_data['auth_user']
            auth_user = CustomUser.objects.get(username=auth_user)
            # print("l'utilisateur est :",auth_user)
            groupe_all = form.cleaned_data['groupe']
            groupe = str(groupe_all)
            groupe = groupe.split("-")
            day = groupe[0]
            time_slot = groupe[1]+"-"+groupe[2]
            date_meeting1 = form.cleaned_data['free_date1']
            date_meeting2 = form.cleaned_data['free_date2']
            date_meeting3 = form.cleaned_data['free_date3']
            # for test
            # print('date_meeting vaut',date_meeting1)
            date_meeting1 = CalendarMeeting.objects.get(date=date_meeting1)
            if date_meeting2 != datetime.date(2020, 1, 1):
                date_meeting2 = CalendarMeeting.objects.get(date=date_meeting2)
            else:
                date_meeting2 = None

            if date_meeting3 != datetime.date(2020, 1, 1):
                date_meeting3 = CalendarMeeting.objects.get(date=date_meeting3)
            else:
                date_meeting3 = None
            groupe = Meeting.objects.get(day=day, time_slot=time_slot)
            exchange_meeting = ExchangeMeeting.objects.update_or_create(
                exchange_operational=False,
                caller=auth_user,
                caller_meeting=call_meeting
            )
            # print('exchange_meeting vaut', exchange_meeting[0].id)
            exchange_meeting_id = ExchangeMeeting.objects.get(
                pk=exchange_meeting[0].id
                )
            list_exchange_meeting = ListExchangeMeeting.objects.update_or_create(
                exchange_meeting=exchange_meeting_id,
                date_meeting1=date_meeting1,
                date_meeting2=date_meeting2,
                date_meeting3=date_meeting3,
                groupe=groupe)
            # send an email to the gange ici simuler par houche.serge@gmail.com
            message = 'Rendez-vous sur le site pour découvrir une demande'
            message = message + ' d\'échange avec votre groupe de modelage du '
            message = message + str(groupe_all)
            message = message + ' à l\'Atelier Terre au Bout des Doigts'
            gang = Gang.objects.filter(meeting_id=groupe)
            mail_user_gang = []
            for gang in gang:
                mail_user_gang.append(gang.auth_user.email)
            mail_gang = ['houche.serge@gmail.com', ]
            obj_message = 'Demande d\'échange de séance sur le site de Terre'
            obj_message = obj_message + ' au bout des doigts'
            send_mail(
                obj_message,
                message,
                'houche.zebra385@gmail.com',
                mail_gang,
                fail_silently=False,
            )
            return redirect("members:confirmcallexchangemeeting")
        else:
            # for test
            # print('form non valid')
            # print(form.errors)
            context = {'form': form}
            return render(request,  self.template_name, context)


@method_decorator(login_required(login_url='login'),
                  name='dispatch')
class CalendarExchangeMeeting(ListView):
    """
    That class to show the possibility of exchange meeting
    """
    model = ExchangeMeeting
    template_name = 'members/calendar_exchange_meeting.html'

    def get_queryset(self):
        self.listexchangemeeting = ListExchangeMeeting.objects.all()
        # print('la listedemande d\'échange sont',self.listexchangemeeting )
        return self.listexchangemeeting

    def get_context_data(self, **kwargs):
        kwargs['listexchangemeeting'] = self.listexchangemeeting
        return super(CalendarExchangeMeeting, self).get_context_data(**kwargs)

    def post(self, request):
        # we take the id of the person who is connect
        auth_user = request.user
        selected_choice = request.POST.get('choice')
        choix_cocher = int(self.request.POST.get('elements'))
        pk = selected_choice
        meeting = ListExchangeMeeting.objects.get(id=pk)
        exchangemeeting = ExchangeMeeting.objects.get(
            pk=meeting.exchange_meeting.id
            )
        if choix_cocher == 1:
            day_listechangemeeting = ListExchangeMeeting.objects.get(
                pk=pk
                ).date_meeting1
        elif choix_cocher == 2:
            day_listechangemeeting = ListExchangeMeeting.objects.get(
                pk=pk
                ).date_meeting2
        elif choix_cocher == 3:
            day_listechangemeeting = ListExchangeMeeting.objects.get(
                pk=pk
                ).date_meeting3
        exchangemeeting.acceptor = CustomUser.objects.get(username=auth_user)
        exchangemeeting.acceptor_meeting = CalendarMeeting.objects.get(
            date=str(day_listechangemeeting)
            )
        exchangemeeting.exchange_operational = True
        exchangemeeting.save()
        # Send a email to inform caller and acceptor than a exchange is valided
        date_caller_meeting = date_french(exchangemeeting.caller_meeting.date)
        date_acceptor_meeting = date_french(
            exchangemeeting.acceptor_meeting.date
            )
        message1 = '(Mme/M.) '
        message1 = message1 + str(exchangemeeting.caller)
        message1 = message1 + ' ,nous vous confirmons  l\'échange'
        message1 = message1 + '  de votre séance du  '
        message1 = message1 + date_caller_meeting + ' avec la séance du '
        message1 = message1 + date_acceptor_meeting + ' de (Mme/M.) '
        message1 = message1 + str(exchangemeeting.acceptor)
        message1 = message1 + ' à l\'Atelier Terre au Bout des Doigts'
        email_caller = [exchangemeeting.caller.email, ]
        obj_message = 'Demande d\'échange de séance sur le site de Terre'
        obj_message = obj_message + ' au bout des doigts'
        send_mail(
            obj_message,
            message1,
            'houche.zebra385@gmail.com',
            email_caller,
            fail_silently=False,
            )
        message2 = '(Mme/M.) ' + str(exchangemeeting.acceptor)
        message2 = message2 + ' ,nous vous confirmons  l\'échange'
        message2 = message2 + ' de votre séance du  '
        message2 = message2 + date_acceptor_meeting + ' avec la séance du '
        message2 = message2 + date_caller_meeting + ' de (Mme/M.) '
        message2 = message2 + str(exchangemeeting.caller)
        message2 = message2 + ' à l\'Atelier Terre au Bout des Doigts'
        email_acceptor = [exchangemeeting.acceptor.email, ]
        obj_message = 'Demande d\'échange de séance sur le site de Terre'
        obj_message = obj_message + ' au bout des doigts'
        send_mail(
            obj_message,
            message2,
            'houche.zebra385@gmail.com',
            email_acceptor,
            fail_silently=False,
        )
        # delete old dates on  the calendars of caller and acceptor 
        caller_calendar = CalendarCustomuser.objects.get(
            auth_user=exchangemeeting.caller,
            date_meeting=exchangemeeting.caller_meeting)
        caller_calendar.delete()
        acceptor_calendar = CalendarCustomuser.objects.get(
            auth_user=exchangemeeting.acceptor,
            date_meeting=exchangemeeting.acceptor_meeting
            )
        acceptor_calendar.delete()
        # Add news dates to  the calendars of caller and acceptor
        # it is a simple change of date_meeting between caller and acceptor
        CalendarCustomuser.objects.create(
            auth_user=exchangemeeting.caller,
            date_meeting=exchangemeeting.acceptor_meeting
            )
        CalendarCustomuser.objects.create(
            auth_user=exchangemeeting.acceptor,
            date_meeting=exchangemeeting.caller_meeting
            )
        # test
        # all_caller_calendar = CalendarCustomuser.objects.
        # filter(auth_user=exchangemeeting.caller).order_by('id')
        # for m in all_caller_calendar:
        # print("customuser ", m.id," le nom est:",
        # m.auth_user,'en date du : ',m.date_meeting)
        # print(' séance du acceptor est changer à la date du : ',
        # acceptor_calendar.date_meeting)
        return redirect("members:confirmacceptexchangemeeting")


@method_decorator(login_required(login_url='login'),
                  name='dispatch')
class ConfirmAcceptExchangeMeeting(TemplateView):
    """
    class to confirm accept exchange meeting
    """
    template_name = 'members/confirm_accept_exchange_meeting.html'


@method_decorator(login_required(login_url='login'),
                  name='dispatch')
class ConfirmCallExchangeMeeting(TemplateView):
    """
    class to confirm  call exchange meeting
    """
    template_name = 'members/confirm_call_exchange_meeting.html'
