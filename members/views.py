from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from members.models import CalendarCustomuser, CalendarMeeting
from accounts.models import CustomUser
from members.create_calendar import day_list
from members.models import  ExchangeMeeting, ListExchangeMeeting, CalendarMeeting, Meeting, Gang
from datetime import date
from members.forms import ExchangeMeetingForm
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.core.mail import send_mail
from members.create_calendar import calendar, calendar_customuser, calendar1
from datetime import date
import datetime 
# Create your views here.


@method_decorator(login_required(login_url='login'),
                  name='dispatch')
class AccueilMemberView(ListView):
    """ That class to get the acceuil page"""
    template_name = "members/accueil_member.html"
    context_object_name = 'calendar_meeting_list'   # your own name for the list as a template variable
    model = CalendarCustomuser
    form = ExchangeMeetingForm

    def get_queryset(self):
        self.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        self.calendar=calendar(self.day_list)
        # load id for the user connect
        auth_user_id=self.request.user
        # load the calendar of this user
        self.day_list_customuser= list(CalendarCustomuser.objects.filter(auth_user=auth_user_id).order_by('date_meeting'))
        self.calendar_user=calendar1(self.day_list_customuser)
        self.calendar_customuser=calendar_customuser(self.calendar_user, self.calendar)


       
           
        return self.calendar, self.calendar_customuser

    def get_context_data(self, **kwargs):
        kwargs['calendar'] = self.calendar
        kwargs['calendar_customuser'] = self.calendar_customuser
       
        return super(AccueilMemberView, self).get_context_data(**kwargs)



@method_decorator(login_required(login_url='login'),
                  name='dispatch')   
class CallExchangeMeeting(View):
    form_class = ExchangeMeetingForm
    template_name = 'members/register_call.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user        
        auth_user=CustomUser.objects.get(pk=user.id)
        form = self.form_class(initial={'auth_user': auth_user, })
        context = {'form': form,}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)        
        if form.is_valid():
            auth_user = self.request.user
            #auth_user=CustomUser.objects.get(pk=user.id)
            call_meeting = form.cleaned_data['call_meeting']
            call_meeting=CalendarMeeting.objects.get(date=call_meeting)
            # auth_user = form.cleaned_data['auth_user']
            auth_user = CustomUser.objects.get(username=auth_user)
            # print("l'utilisateur est :",auth_user)
            groupe_all = form.cleaned_data['groupe']
            groupe = str(groupe_all)
            groupe = groupe.split("-")
            day=groupe[0]
            time_slot=groupe[1]+"-"+groupe[2]
            # print('jour:',groupe[0],'slot:', groupe[1])
            date_meeting1 = form.cleaned_data['free_date1']
            date_meeting2 = form.cleaned_data['free_date2']
            date_meeting3 = form.cleaned_data['free_date3']
            date_meeting1 = CalendarMeeting.objects.get(date=date_meeting1)
            date_meeting2 = CalendarMeeting.objects.get(date=date_meeting2)
            date_meeting3 = CalendarMeeting.objects.get(date=date_meeting3)
            groupe = Meeting.objects.get(day=day ,time_slot=time_slot)
            # print('les dates sont', date_meeting1, date_meeting2, date_meeting3)
            exchange_meeting = ExchangeMeeting.objects.update_or_create(
            exchange_operational=False,
            caller=auth_user,
            caller_meeting=call_meeting
            )
            # print('exchange_meeting vaut', exchange_meeting[0].id)
            exchange_meeting_id=ExchangeMeeting.objects.get(pk=exchange_meeting[0].id)
            list_exchange_meeting=ListExchangeMeeting.objects.update_or_create(
            exchange_meeting=exchange_meeting_id,
            date_meeting1=date_meeting1,
            date_meeting2=date_meeting2,
            date_meeting3=date_meeting3,
            groupe=groupe)
            # envoi d'un email au groupe ici simuler par houche.serge@gmail.com
            message = 'Rendez-vous sur le site pour découvrir une demande d\'échange avec votre groupe de modelage du '+str(groupe_all)+' à l\'Atelier Terre au Bout des Doigts'
            gang = Gang.objects.filter(meeting_id=groupe)
            mail_user_gang=[]
            for gang in gang:
                # print('gang vaut:',gang.auth_user.email)
                mail_user_gang.append (gang.auth_user.email)       
            
            
            mail_gang = ['houche.serge@gmail.com',]
            send_mail(
                'Demande d\'échange de séance sur le site de Terre au bout des doigts',
                message,
                'houche.zebra385@gmail.com',
                mail_gang,
                fail_silently=False,
            )
            
            return redirect("members:confirmcallexchangemeeting")
        else:
            print('form est:non valid')
            print('les erreurs sont',form.errors)
            user = self.request.user
            auth_user=CustomUser.objects.get(pk=user.id)
            form = self.form_class(initial={'auth_user': auth_user, })
            print(form.errors)
            auth_user_id = self.request.user.id
            context = {'form': form}
            return render(request,  self.template_name, context)


@method_decorator(login_required(login_url='login'),
                  name='dispatch')           
class CalendarExchangeMeeting(ListView):
    model = ExchangeMeeting
    template_name = 'members/calendar_exchange_meeting.html'
    # form_class= ListExchangeMeetingForm1()

    def get_queryset(self):
        auth_user_id=self.request.user       
        # self.form_class=ListExchangeMeetingForm1
        self.listexchangemeeting=ListExchangeMeeting.objects.all()
        # print('la listedemande d\'échange sont',self.listexchangemeeting )
        return  self.listexchangemeeting

    def get_context_data(self, **kwargs):        
        kwargs['listexchangemeeting'] = self.listexchangemeeting
        # kwargs['form'] = self.form_class
        return super(CalendarExchangeMeeting, self).get_context_data(**kwargs)


    def post(self, request):
            # we take the id of the person who is connect
        auth_user=request.user
        auth_user_id = int(request.user.id)      
        selected_choice = request.POST.get('choice')    
        choix_cocher=int(self.request.POST.get('elements'))

        # print('mon cchoix est:', selected_choice)
        # print('mon choix de dateest',choix_cocher)

        pk=selected_choice
        meeting=ListExchangeMeeting.objects.get(id=pk)
        # print('meeting.exchange_meeting vaut:',meeting.exchange_meeting.id)
        exchangemeeting=ExchangeMeeting2.objects.get(pk=meeting.exchange_meeting.id)
        # print('exchangemeeting vaut:', exchangemeeting)
        if choix_cocher==1:
            day_listechangemeeting=ListExchangeMeeting.objects.get(pk=pk).date_meeting1
            
        elif choix_cocher==2:
            day_listechangemeeting=ListExchangeMeeting.objects.get(pk=pk).date_meeting2
            
        elif choix_cocher==3:
            day_listechangemeeting=ListExchangeMeeting.objects.get(pk=pk).date_meeting3
            
        
        exchangemeeting.acceptor=CustomUser.objects.get(username=auth_user)
        exchangemeeting.acceptor_meeting=CalendarMeeting.objects.get(date=str(day_listechangemeeting))
        exchangemeeting.exchange_operational=True
        exchangemeeting.save()
        # print('l\'exchange meeting vaut:', exchangemeeting)
        # envoi d'un email pour informer les deux personnes de leur échange de séance
        message1 = '(Mme/M.) '+str(exchangemeeting.caller)+' ,nous vous confirmons  l\'échange de votre séance du  '+str(exchangemeeting.caller_meeting)+' avec la séance du '+str(exchangemeeting.acceptor_meeting)+ ' de (Mme/M.) ' + str(exchangemeeting.acceptor) + ' à l\'Atelier Terre au Bout des Doigts'
        email_caller = [exchangemeeting.caller.email,]
        # print('l\'email du caller est :', email_caller)
        send_mail(
            'Demande d\'échange de séance sur le site de Terre au bout des doigts',
            message1,
            'houche.zebra385@gmail.com',
            email_caller,
            fail_silently=False,
            )
        message2 = '(Mme/M.) ' + str(exchangemeeting.acceptor) +' ,nous vous confirmons  l\'échange de votre séance du  '+str(exchangemeeting.acceptor_meeting)+' avec la séance du ' + str(exchangemeeting.caller_meeting)+ ' de (Mme/M.) '+ str(exchangemeeting.caller) +' à l\'Atelier Terre au Bout des Doigts'
        email_acceptor = [exchangemeeting.acceptor.email,]
        # print('l\'email du acceptor est :', email_acceptor)
        send_mail(
            'Demande d\'échange de séance sur le site de Terre au bout des doigts',
            message2,
            'houche.zebra385@gmail.com',
            email_acceptor,
            fail_silently=False,
        )
        # delete old dates on  the calendars of caller and acceptor by datetime.date(2021, 9, 9)=zero_date
        caller_calendar = CalendarCustomuser.objects.get(auth_user=exchangemeeting.caller, date_meeting=exchangemeeting.caller_meeting)
        print('le caller_calendar est:',caller_calendar)
        # zero_date = CalendarMeeting.objects.get(date=datetime.date(2021, 9, 9))
        # caller_calendar.date_meeting = zero_date
        # caller_calendar.save()
        caller_calendar.delete()
        acceptor_calendar = CalendarCustomuser.objects.get(auth_user=exchangemeeting.acceptor, date_meeting=exchangemeeting.acceptor_meeting)
        print('le acceptor_calendar est:',acceptor_calendar)
        # acceptor_calendar.date_meeting = zero_date
        # acceptor_calendar.save()
        acceptor_calendar.delete()
        # Add news dates to  the calendars of caller and acceptor
        # it is a simple change of date_meeting between caller and acceptor
        CalendarCustomuser.objects.create(auth_user=exchangemeeting.caller, date_meeting=exchangemeeting.acceptor_meeting)      
        CalendarCustomuser.objects.create(auth_user=exchangemeeting.acceptor, date_meeting=exchangemeeting.caller_meeting)
        # test
        # all_caller_calendar = CalendarCustomuser.objects.filter(auth_user=exchangemeeting.caller).order_by('id')
        # for m in all_caller_calendar:
        #     print("customuser ", m.id," le nom est:",m.auth_user,'en date du : ',m.date_meeting)
        # print(' séance du acceptor est changer à la date du : ', acceptor_calendar.date_meeting)
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
   


     
    
