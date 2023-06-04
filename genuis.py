import requests
from bs4 import BeautifulSoup as BS
import json
def get_data(s):
    return json.loads(s.text)
def get(s):
    r = requests.get('https://genius.com/api/search/multi?q='+s)
    url = 'https://genius.com'+get_data(r)['response']['sections'][1]['hits'][0]['result']['api_path']
    soup = BS(requests.get(url).content,'html.parser')
    for div in soup.find_all('div'):
        if div.get('class')==['Lyrics__Container-sc-1ynbvzw-6', 'YYrds']:
            res = ''
            for i in div:
                if str(i)!='<br/>':
                    res+=i.get_text()+'\n'
            return res