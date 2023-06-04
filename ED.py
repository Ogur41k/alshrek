import json
import requests
from datetime import *
import get_nom_by_str
def auth():
    with open('1.json') as json_file:
        session = requests.Session()
        session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
        tmp = session.post('https://dnevnik2.petersburgedu.ru/api/user/auth/login', json=json.load(json_file))
        print(tmp.status_code)
        return session
def get_params(delta=0):
    sl = {'p_page': '1',
    'p_datetime_from': '11.03.2022 00:00:00',
    'p_datetime_to': '13.03.2022 23:59:59',
    'p_educations%5B%5D': '103524'}
    today = date.today()
    sl['p_datetime_to'] = '.'.join(str(today + timedelta(days=6-datetime.today().weekday()-delta)).split('-')[::-1])+'%2023:59:59'
    sl['p_datetime_from'] = '.'.join(str(today - timedelta(days=datetime.today().weekday()+delta)).split('-')[::-1]) + '%2000:00:00'
    s = []
    for i in sl:
        s.append(i + '=' + sl[i])
    return '&'.join(s)
def get_data(s):
    return json.loads(s.text)
def get_task(session,subject):
    j = 0
    while True:
        s = 'https://dnevnik2.petersburgedu.ru/api/journal/lesson/list-by-education?' + get_params(j*7)+'&p_educations%5B%5D=103520'
        r = session.get(s)
        json_data = json.loads(r.text)
        for i in json_data['data']['items']:
            if i['subject_name']==subject:
                for j in i['tasks']:
                    if j['task_name'] != None:
                        return j['task_name']
        j+=1
def get_all_hometask():
    session = auth()
    with open('2.json','r', encoding="utf-8") as json_file2:
        js2 = json.load(json_file2)
        today = (datetime.today().weekday()+2)%7
        answer = {}
        for i in js2[str(today)]:
            answer[i]= get_task(session,i)
        print(answer)
        return answer
def get_rating():
    sl = {}
    session = auth()
    j = 1
    r2 = session.get('https://dnevnik2.petersburgedu.ru/api/journal/estimate/table?p_educations[]=103524&p_date_from=09.01.2022&p_date_to=22.03.2022&p_limit=100&p_page='+str(j))
    data = get_data(r2)
    while data['data']['items']!=[]:
        for i in data['data']['items']:
            if i['estimate_value_name'].isdigit():
                if i['subject_name'] in sl:
                    sl[i['subject_name']]+=[int(i['estimate_value_name'])]
                else:
                    sl[i['subject_name']]=[]
                    sl[i['subject_name']] += [int(i['estimate_value_name'])]
        j+=1
        r2 = session.get(
            'https://dnevnik2.petersburgedu.ru/api/journal/estimate/table?p_educations[]=103524&p_date_from=09.01.2022&p_date_to=22.03.2022&p_limit=100&p_page=' + str(
                j))
        data = get_data(r2)
    return sl
def get_sred_ball():
    sl = get_rating()
    sl1 = {}
    for i in sl:
        sl1[i] = str(round(sum(sl[i])/len(sl[i]),2))
    return sl1
def get_example_task(id):
    session = auth()
    r = session.get('https://dnevnik2.petersburgedu.ru/api/journal/lesson/list-by-subject?p_limit=101&p_page=1&p_datetime_from=01.09.2022&p_datetime_to=31.08.2023&p_educations[]=103524&p_groups[]=314145&p_subjects[]='+str(id))
    data = get_data(r)
    print(data)
    for i in data['data']['items']:
        if i['tasks']!=[]:
            print(i['tasks'][0]['task_name'])
def try_example_task(id,func):
    session = auth()
    r = session.get('https://dnevnik2.petersburgedu.ru/api/journal/lesson/list-by-subject?p_limit=101&p_page=1&p_datetime_from=01.09.2022&p_datetime_to=31.08.2023&p_educations[]=103524&p_groups[]=314145&p_subjects[]='+str(id))
    data = get_data(r)
    for i in data['data']['items']:
        if i['tasks'] != []:
            print(i['tasks'][0]['task_name'])
            print(func(i['tasks'][0]['task_name']))