import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote as decode

def workornot():
    reply = '停班停課資訊如下\n'
    url = 'https://www.dgpa.gov.tw/typh/daily/nds.html'
    resp = requests.get(url) #取得網頁原始碼
    resp.encoding = 'utf8' #轉編碼，才不會出現亂碼
    soup = BeautifulSoup(resp.text, 'html.parser') #利用BeautifulSoup轉換成該套件格式

    city = soup.find_all('td', headers="city_Name") #取得停班課縣市
    detail = soup.find_all('td', headers="StopWorkSchool_Info") #取得停班課資訊

    if city[0].text == '無停班停課訊息。':
        reply = '🚩目前無停班課資訊'
    else:
        for i in range(len(city)):
            reply += '\n' + city[i].text + ':'
            reply += detail[i].text

    reply += '\n\n📊停班停課資訊來自:https://www.dgpa.gov.tw/typh/daily/nds.html'

    return reply
