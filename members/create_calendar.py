from django.db import models
from django.conf import settings
from datetime import date
import datetime 
from django.forms import ModelChoiceField



def calendar(calendar_list):
    
    
    # for day in calendar_list:
    #     print('les dates  calendar sont:',day)
    # make a list by day of week with function day_list
    # and make good list , it add a day 2021-09-09 to have five day by day of week    
    tuesday_list = good_list(day_list(calendar_list,1))
    wenesday_list = good_list(day_list(calendar_list,2))
    thursday_list = good_list(day_list(calendar_list,3))
    # make a new list to have all in the year by order tuesday, wenesdaay and thursday
    regroup_good_list = regroup_list(tuesday_list, wenesday_list,thursday_list)
    # separate list  by month to have  15 days per month
    janary_list = month_list(regroup_good_list,0)
    february_list = month_list(regroup_good_list,1)
    mars_list = month_list(regroup_good_list,2)
    april_list = month_list(regroup_good_list,3)
    may_list = month_list(regroup_good_list,4)
    jun_list = month_list(regroup_good_list,5)

    
    return janary_list, february_list, mars_list, april_list, may_list , jun_list

def day_list(list,number_day_week):
    """function to load the date per day of week and and by month"""
    day_list= []
    
    for day in list:
        #     print('day  de day_list  vaut', day.date)
        day_week = datetime.date(int(day.date.year),int(day.date.month),int(day.date.day)).weekday()
        
        
        if day_week == number_day_week:
            day_list.append(day.date)
   
    return day_list
            
def calendar1(calendar_list):
    
    
    # for day in calendar_list:
    #     print('les dates dans calendar1 sont:',day)
    # make a list by day of week with function day_list
    # and make good list , it add a day 2021-09-09 to have five day by day of week    
    tuesday_list = good_list(day_list1(calendar_list,1))
    wenesday_list = good_list(day_list1(calendar_list,2))
    thursday_list = good_list(day_list1(calendar_list,3))
    # make a new list to have all in the year by order tuesday, wenesdaay and thursday
    regroup_good_list = regroup_list(tuesday_list, wenesday_list,thursday_list)
    # separate list  by month to have  15 days per month
    janary_list = month_list(regroup_good_list,0)
    february_list = month_list(regroup_good_list,1)
    mars_list = month_list(regroup_good_list,2)
    april_list = month_list(regroup_good_list,3)
    may_list = month_list(regroup_good_list,4)
    jun_list = month_list(regroup_good_list,5)

    
    return janary_list, february_list, mars_list, april_list, may_list , jun_list

def day_list1(list,number_day_week):
    """function to load the date per day of week and and by month"""
    day_list= []
    for day in list:
        
        day_week = date(int(day.date_meeting.date.year),int(day.date_meeting.date.month),int(day.date_meeting.date.day)).weekday()
        
        if day_week == number_day_week:
            day_list.append(day.date_meeting.date)
    # for day in day_list:
    #     print('day  de day_list1  vaut', day)       
    return day_list

def good_list(list):
    """function to have 5 day per day_week  by month"""
    counter = 0
    
    while counter <= 15:
        for month in range(0,6):
            for i in range(0+(int(month)*5),5+(int(month)*5)):
                
                try :
                    if int(list[i].month) == 9:
                        pass 
                    elif int(list[i].month) != month+1 and int(list[i].month) != 9:
                        list.insert(i,datetime.date(2021,9,9))
                    counter += 1
                except:
                    list.append(datetime.date(2021,9,9))
                    counter += 1
       
    # test
    # for i in range(25):
    #     print('second',i,list[i])
    #     print(' month',i,list[i].month)
    
        
    return list

def regroup_list(list1,list2,list3):
    regroup_good_list =[]
    for i in range(6):
        begin =int(0 + i*5)
        end = int(5 + i*5)
        regroup_good_list =regroup_good_list + list1[begin:end]+list2[begin:end]+list3[begin:end]
        
    return regroup_good_list
    

def month_list(list,i):
    begin =int(0 + i*15)
    end = int(15 + i*15)
    
    return list[begin:end]



def calendar_customuser(list1,list2):
    # We want to create a dict to know the date of user is true
    list_day = []
    list1_day = []
    list2_day=[]
    
    for day in list1:
        list1_day += day

    print('les dates du user sont',list1_day)
    for day in list2:
        list2_day += day

    print('les dates du calendar sont',list2_day)
    counterdate = 1
    
    counter = 0
    for day_list2 in list2_day:
        count = 0 
        if day_list2 == datetime.date(2021, 9, 9):
            list_day.append(False)
           
            
            count += 1
            counter += 1
            
            
        else :
            for day_list1 in list1_day:
            
                if day_list2 == day_list1 and day_list1 != datetime.date(2021, 9, 9) and count == 0:
                    list_day.append(True)
                    count +=1
                    counter += 1
                    print('counter2= ',counter)
                
        if count == 0:
            list_day.append(False)
            list1_day[counterdate]=datetime.date(2021,9,9)
            print('day ajouter est', list1_day[counterdate])
            counter+= 1
            counterdate += 1
            print('counter3= ',counter)
    counterday = 1
    counterdate =1
    # Now we replace datetime.date(2021,9,9) by date of july in ascending order
    for day in list2_day:
        if day  == datetime.date(2021, 9, 9):
            if counterday <= 31:
                list2_day[counterdate-1]=datetime.date(2021,7,counterday)
                print('day ajouter est', list2_day[counterdate-1])
                counterday += 1
                  
            # Now we replace datetime.date(2021,9,9) by date of aout in ascending order  if july is too litle
            elif counterday >31:
                list2_day[counterdate-1]=datetime.date(2021,8,counterday-30)
                print('day ajouter est', list2_day[counterdate-1])
                counnterday += 1
                       
        counterdate += 1 
            
            


    print('longueur list1', len(list1_day))   
    print('longueur list2', len(list2_day))
    print('longueur list', len(list_day) )     
    # then we create a dict whith the list2_day(list calendar)
    # If date is a date of user we take True, else False
    cles, vals = list2_day, list_day
    dict_list = {a:b for a, b in zip(cles, vals)}
    print('mon dictionaire est:', dict_list)
    dict_list = dict_list.items()
    for key, value   in dict_list:
        print('la clé est:',key,'savaleur: ',value)
    return dict_list