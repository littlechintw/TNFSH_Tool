import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote as decode

def weather_all():

    reply = 'Weather'
    url = 'https://www.cwb.gov.tw/V7/forecast/f_index.htm'
    resp = requests.get(url) #取得網頁原始碼
    resp.encoding = 'utf8' #轉編碼，才不會出現亂碼
    soup = BeautifulSoup(resp.text, 'html.parser') #利用BeautifulSoup轉換成該套件格式

    time = soup.find('div', 'modifyedDatethree')
    area = soup.find_all('td', width="60%")
    temp = soup.find_all('td', width="50%")
    rain = soup.find_all('td', width="18%")
    reply += '\n' + time.text + '\n\n'
    for i in range(len(area)):
        reply += area[i].text + ' ' + temp[i].text + ' ' + ' 降雨機率:' + rain[i].text + '\n'

    return reply
    
print(weather_all())
