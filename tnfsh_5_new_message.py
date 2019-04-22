import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote as decode

def tnfshnew():

    reply = ''

    url = 'https://www.tnfsh.tn.edu.tw/files/501-1000-1012-1.php?Lang=zh-tw'
    resp = requests.get(url)
    resp.encoding = 'utf8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    sesoup = soup.find_all('span', 'ptname ', limit=5)

    for i in range(5):
        reply += str(i+1) + '.'
        #reply += sesoup[i].find('td', string=re.compile('^2')).string.strip('\n').strip(' ')
        reply += sesoup[i].find('a').string.strip('\n').strip('\t').strip(' ')
        reply += sesoup[i].find('a')['href'].strip('\n').strip('\t').strip(' ') + '\n\n'

    return reply
