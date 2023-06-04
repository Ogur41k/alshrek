# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as BS
import docx
import re
def get_answer(query):
    try:
        r =requests.post('https://rus-oge.sdamgia.ru/search',json={'search':query,'cb': '1','body': '3','solution': '1','text': '2','keywords': '10'})
        print(r.status_code)
        soup = BS(r.content,'html.parser')
        print(soup)
        # print(soup.find('div',_class='solution').get_text())
    except:
        None
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
s =getText('1.docx')
s = re.split(r'\d[.]',s)[1:]
for i in s:
    print('\n'.join(i.split('\n')[1:]))
    get_answer('\n'.join(i.split('\n')[1:]))