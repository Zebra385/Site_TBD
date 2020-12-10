from django.db import models
from datetime import date
import datetime

# Create your models here.

def day_list(list,number_day_week):
    """function to load the date per day of week and and by month"""
    day_list= []
    for day in list:
        day_week = date(int(day.date.year),int(day.date.month),int(day.date.day)).weekday()
        
        if day_week == number_day_week:
            day_list.append(day.date)
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