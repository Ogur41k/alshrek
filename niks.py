import requests
from bs4 import BeautifulSoup as BS
def get_random():
    return BS(requests.get('https://vnickname.ru/random.php?').content,'html.parser').find('a',style='font-size:20px;').get_text()