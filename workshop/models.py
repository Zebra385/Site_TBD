from django.db import models
from datetime import date
import datetime


# def calendar(calendar_list):
    
#     # for day in calendar_list:
#     #     print('les dates sont:',day.date)
#     # make a list by day of week with function day_list
#     # and make good list , it add a day 2021-09-09 to have five day by day of week    
#     tuesday_list = good_list(day_list(calendar_list,1))
#     wenesday_list = good_list(day_list(calendar_list,2))
#     thursday_list = good_list(day_list(calendar_list,3))
#     # make a new list to have all in the year by order tuesday, wenesdaay and thursday
#     regroup_good_list = regroup_list(tuesday_list, wenesday_list,thursday_list)
#     # separate list  by month to have  15 days per month
#     janary_list = month_list(regroup_good_list,0)
#     february_list = month_list(regroup_good_list,1)
#     mars_list = month_list(regroup_good_list,2)
#     april_list = month_list(regroup_good_list,3)
#     may_list = month_list(regroup_good_list,4)
#     jun_list = month_list(regroup_good_list,5)

    
#     return janary_list, february_list, mars_list, april_list, may_list , jun_list

# def day_list(list,number_day_week):
#     """function to load the date per day of week and and by month"""
#     day_list= []
#     for day in list:
#         day_week = date(int(day.date.year),int(day.date.month),int(day.date.day)).weekday()
        
#         if day_week == number_day_week:
#             day_list.append(day.date)
#     return day_list
            


# def good_list(list):
#     """function to have 5 day per day_week  by month"""
#     counter = 0
    
#     while counter <= 15:
#         for month in range(0,6):
#             for i in range(0+(int(month)*5),5+(int(month)*5)):
                
#                 try :
#                     if int(list[i].month) == 9:
#                         pass 
#                     elif int(list[i].month) != month+1 and int(list[i].month) != 9:
#                         list.insert(i,datetime.date(2021,9,9))
#                     counter += 1
#                 except:
#                     list.append(datetime.date(2021,9,9))
#                     counter += 1
       
#     # test
#     # for i in range(25):
#     #     print('second',i,list[i])
#     #     print(' month',i,list[i].month)
     
        
#     return list

# def regroup_list(list1,list2,list3):
#     regroup_good_list =[]
#     for i in range(6):
#         begin =int(0 + i*5)
#         end = int(5 + i*5)
#         regroup_good_list =regroup_good_list + list1[begin:end]+list2[begin:end]+list3[begin:end]
        
#     return regroup_good_list
    

# def month_list(list,i):
#     begin =int(0 + i*15)
#     end = int(15 + i*15)
    
#     return list[begin:end]