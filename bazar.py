import requests
from bs4 import BeautifulSoup as BS
def get():
    sl = {'делать варшаву':'сравнять человека с землей, уничтожить его. Это выражение появилось после войны в уголовных нацистских лагерях'}
    r = requests.get('https://ru.wiktionary.org/wiki/%D0%9F%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5:%D0%A3%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BD%D1%8B%D0%B9_%D0%B6%D0%B0%D1%80%D0%B3%D0%BE%D0%BD')
    soup = BS(r.content,'html.parser')
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            try:
                key = li.find('b').get_text()
                value = li.get_text().split('—')[1].replace('.','')
                sl[key.lower()]=value
            except:
                try:
                    key = li.find('b').get_text()
                    value = li.get_text().split('-')[1].replace('.', '')
                    sl[key.lower()] = value
                except :
                    None
    return sl