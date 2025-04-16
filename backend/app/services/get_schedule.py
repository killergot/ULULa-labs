from app.database.psql import get_db
from app.crud.schedule import ScheduleService
import json
from datetime import datetime, timedelta
from app.database.models.schedule import Schedule
from app.database.models.students import Student
from app.database.models.tasks import Task
from app.crud.students import StudentService

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

def load_schedule_for_group(group):
    zaproc = requests.get(f'https://ruz.spbstu.ru/search/groups?q={group}')
    soup = BeautifulSoup(zaproc.text, "lxml")
    groups = soup.find_all('a', class_='groups-list__link')
    date = datetime.now()
    for url in groups:
        url_strok = list(url['href'])
        break

    url_strok_itog=url_strok[-5:]
    id_itog = {}
    id_itog="".join(url_strok_itog)

    for i in range (1, 5):
        zaproc = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{id_itog}?date={date.strftime("%Y-%m-%d")}')
        data = zaproc.json()

        print("hello", data)
        result = []
        schedule=[]
        sunday={}
        monday={}
        tuesday={}
        wednesday={}
        thursday={}
        friday={}
        saturday={}
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
                monday = day_info['lessons']
            if day_info['weekday']==2:
                tuesday = day_info['lessons']
            if day_info['weekday'] == 3:
                wednesday = day_info['lessons']
            if day_info['weekday'] == 4:
                thursday = day_info['lessons']
            if day_info['weekday'] == 5:
                friday = day_info['lessons']
            result.append(day_info)
    #в бд для каждого дня недели добавляем lessons

        print ('\n\n\n\n', monday)
        result = json.dumps(result, ensure_ascii=False)
        try:
            if ScheduleService.is_schedule_exist(next(get_db()), group, i):
                schedule = ScheduleService.update_schedule(next(get_db()), group, i, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
            else:
                schedule = ScheduleService.create_schedule(next(get_db()), group, i, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
            print(schedule)
        except Exception as e:
            print({"Schedule update error": e})
        date = date + timedelta(days=7)
#+++ #1 - сделать, чтобы для 1 группы добавлялось в БД 1 неделя +++
#+++ 2 - 4 недели +++
#3 - для выбранной группы
#4 - проход по всем группам
#5 - ручка ap



def load_all_schedule():
    groups = StudentService.read_groups(next(get_db()))
    for group in groups:
        print (group[0])
        load_schedule_for_group(group[0])

load_all_schedule()