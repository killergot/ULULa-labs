#from app.database.psql import get_db
#from app.crud.schedule import ScheduleService
import json
from datetime import datetime, timedelta
from app.database.models.schedule import Schedule
from app.database.models.students import Student
from app.database.models.tasks import Task
from app.shemas.schedule import  ScheduleIn, ScheduleBase
#Получаем расписание для 4 недель
#Для каждой уникальной группы?
#Раз в день +при добавлении новой группы???

#парсим для текущей даты + 7 дней + 7 дней + 7 дней
#как складывать даты и корректно нереходить на следующий месяц

#получаем расписание на неделю

#из него берём названия и время, составляем json для каждого дня

import requests
from bs4 import BeautifulSoup

#date = input("Введите дату: ")
#group = input("Введите номер группы: ")


def load_schedule_for_all_groups():
    all_schedule = {}
    groups_list = []
    for v in range (1, 10):
      #  v=51003 # временная заглушка
        zaproc = requests.get(f'https://ruz.spbstu.ru/search/groups?q={v}/')
        soup = BeautifulSoup(zaproc.text, "lxml")
        groups = soup.find_all('a', class_='groups-list__link')
        date = datetime.now()
        i=0
        print (groups)
        for url in groups:
            print (url)
            i=i+1
            start = str(url).find('>')+1
            end = str(url).find('</a>')
            group_number= str(url)[start:end]
            #print(link_text)
            url_strok = list(url['href'])
            url_strok_itog = url_strok[-5:]
            id_itog = {}
            id_itog = "".join(url_strok_itog)
           # print(i, "gr_num: ", group_number)
            groups_list.append(id_itog)
            #print(len(groups_list))
            load_schedule_for_group(id_itog, group_number)
   # print ("final", len(groups_list))

    return groups_list


def load_group_list():
    all_schedule = {}
    groups_list = []
    for v in range (1, 10):
      #  v=51003 # временная заглушка
        zaproc = requests.get(f'https://ruz.spbstu.ru/search/groups?q={v}/')
        soup = BeautifulSoup(zaproc.text, "lxml")
        groups = soup.find_all('a', class_='groups-list__link')

        date = datetime.now()
        i=0
        #print (groups)
        for url in groups:
            #print (url)
            i=i+1
            start = str(url).find('>')+1
            end = str(url).find('</a>')
            group_number= str(url)[start:end]
            groups_list.append(group_number)
            #print(len(groups_list))
    #print ("final", len(groups_list))

    return groups_list

def load_schedule_for_group(group_number, week_number, group_id):
    zaproc = requests.get(f'https://ruz.spbstu.ru/search/groups?q={group_number}')
    soup = BeautifulSoup(zaproc.text, "lxml")
    groups = soup.find_all('a', class_='groups-list__link')
    date = datetime.now()
    for url in groups:
        url_strok = list(url['href'])
        break

    url_strok_itog = url_strok[-5:]
    id_itog = {}
    id_itog = "".join(url_strok_itog)

    date = datetime.now()+ timedelta(days=7)*week_number
    for i in range (1, 2):
        zaproc = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{id_itog}?date={date.strftime("%Y-%m-%d")}')
        data = zaproc.json()
        print("hello", data)
        result = []
        schedule=[]
        sunday=[]
        monday=[]
        tuesday=[]
        wednesday=[]
        thursday=[]
        friday=[]
        saturday=[]
        for day in data['days']:

            day_info = {
                'weekday': day['weekday'],
                'date': day['date'],
                'lessons': []
            }

            for lesson in day['lessons']:

                lesson_info = {

                    'subject': lesson['subject'],

                    'time_start': lesson['time_start'],

                    'time_end': lesson['time_end'],
                    'teacher': "unknown",
                    'place': "unknown"

                }
                if lesson['teachers']:
                    lesson_info['teacher']=lesson['teachers'][0]['full_name']
                if lesson['auditories']:
                    lesson_info['place']=lesson['auditories'][0]['building']['name']+', к. ' +lesson['auditories'][0]['name']

                day_info['lessons'].append(lesson_info)
            if day_info['weekday']==1:
                monday.append(day_info['lessons'])
            if day_info['weekday']==2:
                tuesday.append(day_info['lessons'])
            if day_info['weekday'] == 3:
                wednesday.append(day_info['lessons'])
            if day_info['weekday'] == 4:
                thursday.append(day_info['lessons'])
            if day_info['weekday'] == 5:
                friday.append(day_info['lessons'])
            if day_info['weekday'] == 6:
                saturday.append(day_info['lessons'])
            result.append(day_info)
          #  print('\n\n\n\n', monday)
        try:
            final = ScheduleBase.model_validate({"group_id": group_id, "week_number": i, "monday": monday, "tuesday": tuesday, "wednesday": wednesday, "thursday": thursday, "friday": friday, "saturday": saturday, "sunday": sunday})
          #  print(final)
        except Exception as e:
            print("Error during validate", e)
        return final


    