from django.shortcuts import render
from django.views.generic import ListView, View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from members.models import CalendarCustomuser
from workshop.models import good_list, regroup_list, month_list
from members.models import day_list
from datetime import date
from members.forms import EchangeMeetingForm

# Create your views here.






@method_decorator(login_required(login_url='login'),
                  name='dispatch')
class AccueilMemberView(ListView):
    """ That class to get the acceuil page"""
    template_name = "members/accueil_member.html"
    context_object_name = 'calendar_meeting_list'   # your own name for the list as a template variable
    model = CalendarCustomuser
    form = EchangeMeetingForm

   
    def get_queryset(self):
        # load id for the user connect
        auth_user_id=self.request.user
        # load the calendar of this user
        self.day_list = CalendarCustomuser.objects.filter(auth_user=auth_user_id)
        for day in self.day_list:
            print(day.date_meeting)
        # make a list by day of week with function day_list
        # and make good list , it add a day 2021-09-09 to have five day by day of week    
        self.tuesday_list = good_list(day_list(self.day_list,1))
        self.wenesday_list = good_list(day_list(self.day_list,2))
        self.thursday_list = good_list(day_list(self.day_list,3))
        # make a new list to have all in the year by order tuesday, wenesdaay and thursday
        self.regroup_list= regroup_list(self.tuesday_list, self.wenesday_list,self.thursday_list)
        # separate list  by month to have  15 days per month
        self.janary_list = month_list(self.regroup_list,0)
        self.february_list = month_list(self.regroup_list,1)
        self.mars_list = month_list(self.regroup_list,2)
        self.april_list = month_list(self.regroup_list,3)
        self.may_list = month_list(self.regroup_list,4)
        self.jun_list = month_list(self.regroup_list,5)

       
        return self.janary_list, self.february_list, self.mars_list, self.april_list, self.may_list , self.jun_list

    def get_context_data(self, **kwargs):
        kwargs['janary_list'] = self.janary_list
        kwargs['february_list'] = self.february_list
        kwargs['mars_list'] = self.mars_list
        kwargs['april_list'] = self.april_list
        kwargs['may_list'] = self.may_list
        kwargs['jun_list'] = self.jun_list

        # print('Liste de janvier:',self.janary_list)
        # print('Liste de fevrier:',self.february_list)
        # print('Liste de mars:',self.mars_list)
        # print('Liste de avril:',self.april_list)
        # print('Liste de mai:',self.may_list)
        # print('Liste de juin:',self.jun_list)
       

        return super(AccueilMemberView, self).get_context_data(**kwargs)
    
class CallExchangeMetting(View):
    form_class = EchangeMeetingForm
    template_name = 'members/register_call.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # recup donnée
            return HttpResponseRedirect("/")
        else:
            print('form est:non valid')
            print(form.errors)
            context = {'form': form}
            return render(request,  self.template_name, context)
        