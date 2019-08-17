import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote as decode
import json

def weather_all_beta():
    reply = '測站資訊：\n'
    reply += '(地區) (溫度) (濕度) (天氣狀況)'

    url = 'https://www.cwb.gov.tw/Data/js/Observe/Observe_Home.js?'
    resp = requests.get(url) #取得網頁原始碼
    resp.encoding = 'utf8' #轉編碼，才不會出現亂碼
    soup = BeautifulSoup(resp.text, 'html.parser') #利用BeautifulSoup轉換成該套件格式
    gettime = str(soup)[19:30] #取得此資料的時間
    
    gettextf = str(soup).find('OBS = ') + 6 #將資料轉成json格式(開始)
    soup = str(soup)[gettextf:].replace('};','}')

    for i in range(0,10):
        nn = soup.find(str(i) + ':{')
        soup = soup[:nn-1] + '\'' + str(i) + '\'' + soup[nn+1:]

    for i in range(10,15):
        nn = soup.find(str(i) + ':{')
        soup = soup[:nn-1] + '\'' + str(i) + '\'' + soup[nn+2:]

    soup = soup.replace('\'', '\"') #將資料轉成json格式(結束)
    jsondata = json.loads(soup) #將資料轉成json字典

    for i in range(len(jsondata)):
        reply += '\n' + jsondata[str(i)]['CountyName']['C'] + ' ' 
        if(jsondata[str(i)]['Temperature']['C']=='-'):
            reply += jsondata[str(i)]['Temperature']['C'] + '    '
        else:
            reply += jsondata[str(i)]['Temperature']['C'] + '℃'

        if(jsondata[str(i)]['Humidity']=='-'):
            reply += ' ' + jsondata[str(i)]['Humidity'] + '  '
        else:
            reply += ' ' + jsondata[str(i)]['Humidity'] + '%'
            
        reply += ' ' + jsondata[str(i)]['Weather']['C']
        
    reply += '\n\n資料時間' + gettime

    return reply
    
print(weather_all_beta())
