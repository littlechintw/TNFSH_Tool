import json
import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote as decode

def classstate(time_start, time_end, user_class, user_sitenum):
    # time form 2019-04-06
    namedata = '{"3":"早自修", "4":"第一節", "5":"第二節", "6":"第三節", "7":"第四節", "8":"午休", "9":"第五節", "10":"第六節", "11":"第七節", "12":"第八節"}'
    jsonnd = json.loads(namedata)

    reply = '查詢區間:' + time_start + '至' + time_end + '\n\n'
    url = 'https://sp.tnfsh.tn.edu.tw/attend/index.php/attend/search?begin=' + time_start + '&end=' + time_end+ '&class=' + user_class +'&num=' + user_sitenum
    resp = requests.get(url) #取得網頁原始碼
    resp.encoding = 'utf8' #轉編碼，才不會出現亂碼
    soup = BeautifulSoup(resp.text, 'html.parser') #利用BeautifulSoup轉換成該套件格式

    formbody = soup.find('tbody')
    detail = formbody.find_all('tr')
    num_of_search = 0
    for i in range(0,len(detail),1):
        if str(detail[i]).find('缺席') >= 0 or str(detail[i]).find('遲到') >= 0 or str(detail[i]).find('早退') >= 0:
            moredet = detail[i].find_all('td')
            reply += moredet[0].text + '\n'
            for j in range(3,13,1):
                if str(moredet[j]).find('缺席') >= 0 or str(moredet[j]).find('遲到') >= 0 or str(moredet[j]).find('早退') >= 0:
                    reply += jsonnd[str(j)] + '-' + moredet[j].text.strip('\n') + '\n'
                    num_of_search += 1
    if num_of_search == 0:
        reply += '太好了，沒有任何異常紀錄呢！'
    else:
        reply += '\n本次查詢共有' + str(num_of_search) + '筆異常紀錄噢，趕緊處理吧！'

    reply += '\n\n不放心嗎？打開以下連結檢查吧！\n' + url
    return reply
