import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote as decode

def earthquake():

    reply = 'Earthquake Report\n\n'

    url = 'https://www.cwb.gov.tw/V7/modules/MOD_EC_Home.htm'
    resp = requests.get(url) #取得網頁原始碼
    resp.encoding = 'utf8' #轉編碼，才不會出現亂碼
    soup = BeautifulSoup(resp.text, 'html.parser') #利用BeautifulSoup轉換成該套件格式

    alldata = soup.find('table')
    onebyone = alldata.find_all('tr', limit=6) #因為第一筆資料是表格頂，所以取需要的數量+1
    for i in range(1,len(onebyone),1):
        detail = onebyone[i].find_all('td')
        reply += '編號:' + detail[0].text
        reply += '\n時間:' + detail[1].text
        reply += '\n規模:' + detail[4].text
        reply += '\n深度:' + detail[5].text + 'km'
        reply += '\n位置:' + detail[6].text.strip('\n')
        reply += '\n震央:' + 'https://www.google.com/maps/search/' + detail[2].text + '%20' + detail[3].text
        reply += '\n\n'

    return reply

print(earthquake())
