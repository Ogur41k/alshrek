import requests
from bs4 import BeautifulSoup as BS

def get_images_mega(url:str):
    links = []
    r = requests.get(url).content
    soup = BS(r,'html.parser')
    for imgtag in soup.find_all('img'):
        if imgtag['src'][:47] == 'https://megaresheba.ru/attachments/images/tasks':
            links.append(imgtag['src'])
    return links

def algebra(nom:str):
    url = f'https://megaresheba.ru/gdz/algebra/9-klass/makarichev-uglublennoe-izuchenie/{nom}-nomer'
    return get_images_mega(url)
def fizika_sborbik(nom:str):
    url = f'https://megaresheba.ru/gdz-sbornik-zadach-po-fizike-10-11-klass-rymkevich/{nom}-nomer'
    return get_images_mega(url)
def fizika(nom:str):
    i = 1
    flag1=True
    links = []
    while flag1:
        url = 'https://megaresheba.ru/index/06/0-371/'+nom+'-'+str(i)+'-nomer'
        t = get_images_mega(url)
        if t==[]:
            flag1=False
        else:
            links+=t
            i+=1
    return links
def russian(nom:str):
    url = f'https://megaresheba.ru/gdz/russkij-yazyk/9-klass/ribchenkova/1-{nom}-nomer'
    return get_images_mega(url)
def litra(nom:str):
    url = f'https://megaresheba.ru/gdz/literatura/9-klass/korovina/{nom}-chast'
    return get_images_mega(url)
def obshestvo(nom:str):
    url = f'https://megaresheba.ru/gdz/obshhestvoznanie/9-klass/bogolyubov/{nom}-paragraph'
    return get_images_mega(url)
