import aiohttp
import asyncio
from datetime import datetime, timedelta
import re
import json

from app.database.models.schedule import Schedule
from app.database.models.students import Student
from app.database.models.tasks import Task
from app.shemas.schedule import  ScheduleIn, ScheduleBase
from app.shemas.teacher_subject import  TeacherSubjectIn
from app.shemas.group_subject import  GroupSubjectIn
import  logging


log = logging.getLogger(__name__)

#Получаем расписание для 4 недель
#Для каждой уникальной группы?
#Раз в день +при добавлении новой группы???

#парсим для текущей даты + 7 дней + 7 дней + 7 дней
#как складывать даты и корректно нереходить на следующий месяц

#получаем расписание на неделю

#из него берём названия и время, составляем json для каждого дня

import requests
from bs4 import BeautifulSoup

# получение расписания для одного преподавателя
async def load_teacher_schedule_module(session, teacher):
    #из объекта препода получить фио и id
    #print(teacher)
    FIO = teacher['FIO']
    id = teacher['id']
    date = datetime.now()
    rezult = []
    #найти препода по ФИО
    url = f'https://ruz.spbstu.ru/search/teacher?q={FIO}'
    try:
        async with session.get(
            url
        ) as response:
            zaproc = await response.text()
            soup = BeautifulSoup(zaproc, "lxml")
            teachers = soup.find_all('a', class_='search-result__link')
           # print(teachers)

            for url in teachers:
                url_strok = url['href']
                break
           # print (url_strok)
            url_strok_itog = url_strok.split('/')[-1]
           # print(url_strok_itog)
            id_itog = "".join(url_strok_itog)
    except Exception as e:
        print("Error(((: ", e, "\n", FIO, date)

    for i in range (1, 5):
        url = f'https://ruz.spbstu.ru/teachers/{id_itog}?date={date.strftime("%Y-%m-%d")}'
        try:
            async with session.get(
                url
            ) as response:
                content_type = response.headers.get('Content-Type', '')
                # print(content_type)
                html = await response.text()

                # Ищем JSON в HTML
                soup = BeautifulSoup(html, 'html.parser')
                script = soup.find('script', string=re.compile('window.__INITIAL_STATE__'))

                if not script:
                    raise ValueError("Не удалось найти window.__INITIAL_STATE__")

                # Извлекаем JSON
                json_text = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script.string, re.DOTALL).group(1)
                data = json.loads(json_text)
                #soup = BeautifulSoup(zaproc, "html")
                #print("hello", data)
                result = []
                schedule=[]
                sunday=[]
                monday=[]
                tuesday=[]
                wednesday=[]
                thursday=[]
                friday=[]
                saturday=[]
                # print(data['teacherSchedule'])
                #print("schedule: ", data['teacherSchedule'])
                schedule = data['teacherSchedule']
                #print(schedule)
                info = schedule['data']

                for day in info[id_itog]:

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
                                'place': "unknown",
                                'groups': []
                                }
                                if lesson['groups']:
                                    for group in lesson['groups']:
                                        lesson_info['groups'].append(group['name'])
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
                    final = ({"teacher_id": id, "week_number": i, "monday": monday, "tuesday": tuesday, "wednesday": wednesday, "thursday": thursday, "friday": friday, "saturday": saturday, "sunday": sunday})
                    #print(group_number)
                    rezult.append(final)

                   # return final

                except Exception as e:
                    print("Error during validate", e)

        except Exception as e:
            print("Error: ",  e, '\n', FIO)

        date = date +timedelta(weeks=i)
    #print(rezult)
    return rezult




# сделать асинхронное получение списка групп
# сделать асинхронное получение расписания студентов по этому списку
# сделать асинхронное получение расписания преподов

#из расписания преподов парсить списки предметов, списки групп для каждого препода


async def load_group_schedule(session, group):
    # загрузка расписания для групп, здесь всё ломается
    group_number = group['group_number']
    group_id = group['group_id']
    date = datetime.now()
    rezult = []
    subjects = []
    teacher_subject = []
    group_subject = []
    id_itog = "38749"
    url = f'https://ruz.spbstu.ru/search/groups?q={group_number}'
    try:
        async with session.get(
            url
        ) as response:
            zaproc = await response.text()
            soup = BeautifulSoup(zaproc, "lxml")
            groups = soup.find_all('a', class_='groups-list__link')
        #date = datetime.now()
            for url in groups:
                url_strok = list(url['href'])
                break
            url_strok_itog = url_strok[-5:]
            id_itog = "".join(url_strok_itog)
    except Exception as e:
        print("Error: ", e, "\n", group_number, date)
        print("Schedule for group ", group_number, " will be replace by fake")

    for i in range (1, 5):
        url = f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{id_itog}?date={date.strftime("%Y-%m-%d")}'
        try:
            async with session.get(
                url
            ) as response:
                data = await response.json()
                soup = BeautifulSoup(zaproc, "lxml")
                #print("hello", data)
                result = []
                schedule=[]
                sunday=[]
                monday=[]
                tuesday=[]
                wednesday=[]
                thursday=[]
                friday=[]
                saturday=[]
                if data['days']:
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
                            subjects.append({'name': lesson['subject']})
                            if lesson['groups']:
                                for group in lesson['groups']:
                                    group_subject.append(GroupSubjectIn.model_validate({'group_number': group['name'], 'subject': lesson['subject']}))
                            if lesson['teachers']:
                                lesson_info['teacher']=lesson['teachers'][0]['full_name']
                                teacher_subject.append(TeacherSubjectIn.model_validate({'FIO': lesson['teachers'][0]['full_name'], 'subject': lesson['subject']}))
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
                    #print(group_number)
                    rezult.append(final)

                   # return final

                except Exception as e:
                    print("Error during validate", e)

        except Exception as e:
            print("Error: ",  e, '\n', group_number)

        date = date +timedelta(weeks=i)

    return (rezult, subjects, teacher_subject, group_subject)


async def get_schedule(groups: list)->tuple:
    # параллелим загрузку расписания
    current_date = datetime.now()
    batch_size = 130
    result = []  # итоговый список
    # распараллелить на потоки
    connector = aiohttp.TCPConnector(limit=100)
    semaphore = asyncio.Semaphore(100)
    schedule = []
    subjects = []
    async with semaphore:
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=100000)) as session:
            tasks = [load_group_schedule(session, group_id) for group_id in groups]
            result = await asyncio.gather(*tasks)

            schedule = [item[0] for item in result]
            all_subjects = [item[1] for item in result]
            all_teacher_subjects = [item[2] for item in result]
            all_group_subjects = [item[3] for item in result]
            unique_subjects = []
            unique_teacher_subjects = []
            unique_group_subjects = []
            for subjects in all_subjects:
                for subject in subjects:
                    unique_subjects.append(subject)

            for teacher_subjects in all_teacher_subjects:
                for teacher_subject in teacher_subjects:
                        unique_teacher_subjects.append(teacher_subject)

            for group_subjects in all_group_subjects:
                for group_subject in group_subjects:
                        unique_group_subjects.append(group_subject)


            return schedule, unique_subjects, unique_teacher_subjects, unique_group_subjects
            # поделить список групп для параллельной обработки
            #for i in range(0, len(groups), batch_size):
              #  batch = groups[i:i + batch_size]
               # batch_results = await load_batch_schedule(session, batch)
               # print (batch_results)

    # создаём 20 задач (выбираем с интервалом 20 элементы списка групп)
    # внутри грузим расписание для каждого из этих наборов и для одной из 4 недель)



async def get_groups()->list[str]:
    current_date = datetime.now()
    result = [] #тоговый список
    # распараллелить на 10 потоков, каждый ищет по цифре от 0 до 9
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Создаем задачи для всех групп
        tasks = [get_groups_module(session, i, result)
                 for i in range (0, 10)]

        all_data = await asyncio.gather(*tasks)
        for data in all_data:
            result.extend(data)
        return  result
    # возвращаем список номеров групп и их внутриполикековских id


async def get_groups_module(session, number: int, result: list):
    # получаем список групп по конкретному значению позиции и дате
    url = f'https://ruz.spbstu.ru/search/groups?q={number}/'
    async with session.get(
            url
    ) as response:
        zaproc = await response.text()
        soup = BeautifulSoup(zaproc, "lxml")
        groups = soup.find_all('a', class_='groups-list__link')
        final = []
        for url in groups:
            start = str(url).find('>') + 1
            end = str(url).find('</a>')
            group_number = str(url)[start:end]
            final.append(group_number)
        await asyncio.sleep( 0.5)
        return final


async def load_group_list():
    id_itog = {}
    all_schedule = {}
    groups_list = []
    for v in range (1, 10):
      #  v=51003 # временная заглушка
        zaproc = requests.get(f'https://ruz.spbstu.ru/search/groups?q={v}/')
        soup = BeautifulSoup(zaproc.text, "lxml")
        groups = soup.find_all('a', class_='groups-list__link')

        date = datetime.now()
        #print (groups)
        for url in groups:
            #print (url)
            start = str(url).find('>')+1
            end = str(url).find('</a>')
            group_number= str(url)[start:end]
            groups_list.append(group_number)
            #print(len(groups_list))
    #print ("final", len(groups_list))

    return groups_list

async def get_teacher_schedule(teachers: list):
    result = []  # тоговый список
    # распараллелить на 10 потоков, каждый ищет по цифре от 0 до 9
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Создаем задачи для всех групп
        tasks = [load_teacher_schedule_module(session, teacher)
                 for teacher in teachers]
        all_data = await asyncio.gather(*tasks)
        unique_teacher_schedules = []
        for teacher_schedules in all_data:
            for teacher_schedule in teacher_schedules:
                unique_teacher_schedules.append(teacher_schedule)
    return unique_teacher_schedules

async def main():
    #result = load_group_list()
    #print (len(result))
    #print (result)
    await get_teacher_schedule([{'FIO': 'Масликов Владимир Иванович', 'id': 4016}])


if __name__ == '__main__':
    asyncio.run(main())






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
        #print (groups)
        for url in groups:
            #print (url)
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
            load_schedule_for_group(id_itog, group_number, i)
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
        #print("hello", data)
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
            final = ScheduleBase.model_validate({"group_id": group_id, "week_number": week_number, "monday": monday, "tuesday": tuesday, "wednesday": wednesday, "thursday": thursday, "friday": friday, "saturday": saturday, "sunday": sunday})
          #  print(final)
        except Exception as e:
            print("Error during validate", e)
        return final

