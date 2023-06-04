import requests
from bs4 import BeautifulSoup as BS
import json
def get_data(s):
    return json.loads(s.text)
def get_reaction(s:str):
    try:
        s = '+%2B+'.join(s.split('+')).replace(' ', '').replace('О', 'O').replace('С', 'C')
        link = f'https://chemequations.com/ru/?s={s}&ref=input'
        html = requests.get(link).content
        soup = BS(html, features="html.parser")
        if 'Существует несколько решений' not in soup.get_text():
            s = ''
            if 'Это окислительно-восстановительная (редокс) реакция:' in soup.get_text():
                for div in soup.find_all('div'):
                    if div.get('class')==['redox-block']:
                        s = '\n'
                        for i in div.find_all('p'):
                            s+=i.get_text()+'\n'
            return soup.find('h1').get_text().replace('(aq)','').replace('(l)','').replace('(s)','').replace('(g)','') + s
        else:
            for i in soup.find_all('td'):
                if str(i)[5]=='a':
                    return i.get_text().replace('(aq)','').replace('(l)','').replace('(s)','').replace('(g)','')

    except:
        return 'Чё то ты перепутал'
def get_seq_reaction(s:str):
    try:
        s = [i.replace(' ', '').replace('О', 'O').replace('С', 'C') for i in s.split('-')]
        ans = []
        for i in range(len(s)-1):
            link = f'https://chemequations.com/ru/advanced-search/?reactant1={s[i]}&product1={s[i+1]}&submit='
            html = requests.get(link).content
            soup = BS(html, features="html.parser")
            for div in soup.find_all('div'):
                if div.get('class')==['search-results-async']:
                    product,reactant = div.get('data-productids'),div.get('data-reactantids')
                    res = get_data(requests.get(f'https://chemequations.com/api/search-reactions-by-compound-ids?reactantIds={reactant}&productIds={product}&offset=0'))
                    ans.append(res['searchResults'][0]['equationStr'])
        return '\n'.join([get_reaction(i) for i in ans])
    except:
        return 'Фраер ты чё берега попутал?'