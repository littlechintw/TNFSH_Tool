# !/usr/bin/env python
# coding=utf-8

import json
import requests
from flask import Flask, request
import re
from urllib.parse import unquote as decode
import urllib.parse
import time
import csv

def take_mask(zipcode):
    logs_yellow('===Processing===')
    CSV_URL = 'http://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D50001-001&l=https://data.nhi.gov.tw/resource/mask/maskdata.csv'
    res = ''
    with requests.Session() as s:
        fullareanum = 0                      # 全部地點
        print_data = 0                       # 處理後資料筆數
        areaname = zipcode_to_area(zipcode)  # 地區名稱
        tw_mask_num = 0                      # 全台成人口罩數量
        tw_mask_num_k = 0                    # 全台兒童口罩數量
        area_mask_num = 0                    # 地區成人口罩數量
        area_mask_num_k = 0                  # 地區兒童口罩數量
        area_havemask = 0                    # 地區有販售成人口罩門市數量
        area_nothavemask = 0                 # 地區有販售兒童口罩門市數量
        if areaname == -1:
            return '錯誤！查無此郵遞區號。'

        download = s.get(CSV_URL) # 下載 csv 檔案
        logs_green('===Download completed===')
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        data_num = len(my_list) - 1 # 計算欄位數量
        
        for row in range(1, data_num): # 計算相關數值
            # print(my_list[row])
            if my_list[row][2].find(areaname) >= 0:
                if int(my_list[row][4])>0:
                    area_havemask+=1
                    if int(my_list[row][4])>10 and print_data<10:
                        # res += '(' + my_list[row][0] + ') '
                        res += my_list[row][1] + '\n'
                        res += my_list[row][2] + '\n'
                        res += my_list[row][3] + '\n'
                        res += '成人口罩剩餘 ' + my_list[row][4] + ' 副\n'
                        res += '兒童口罩剩餘 ' + my_list[row][5] + ' 副\n'
                        res += '來源資料時間: ' + my_list[row][6] + '\n'
                        res += '--------------------\n'
                        print_data+=1
                else:
                    area_nothavemask+=1
                fullareanum+=1
                area_mask_num += int(my_list[row][4])
                area_mask_num_k += int(my_list[row][5])
            tw_mask_num += int(my_list[row][4])
            tw_mask_num_k += int(my_list[row][5])

        # 醫事機構代碼	醫事機構名稱	醫事機構地址	醫事機構電話	成人口罩總剩餘數	兒童口罩剩餘數	來源資料時間

        detail_text  = '全台共有 ' + str(data_num) + ' 個地點還有在販售\n'
        detail_text += '全台成人口罩總數共 ' + str(tw_mask_num) + ' 副\n'
        detail_text += '全台兒童口罩總數共 ' + str(tw_mask_num_k) + ' 副\n'
        detail_text += '\n'
        detail_text += '在 [ ' + areaname + ' ] 共有 ' + str(fullareanum) + ' 個地點還有在販售\n'
        detail_text += '本區成人口罩總數共 ' + str(area_mask_num) + ' 副\n'
        detail_text += '本區兒童口罩總數共 ' + str(area_mask_num_k) + ' 副\n'
        detail_text += '本區共有' + str(area_havemask)    + ' 個地點仍有成人口罩\n'
        # detail_text += str(area_nothavemask) + ' 個地點之成人口罩已售完\n' #但尚有兒童口罩
        print(detail_text)

        if print_data==0:
            res = '錯誤！在 ' + str(data_num)  + ' 筆資料上發現 [ ' + areaname + ' ] 內口罩可能已賣光或剩餘數量皆不足 10 副！。'
        else:
            front_res = '以下僅顯示前 ' + str(print_data) + ' 筆尚有 10 副成人口罩以上之販售地點資料\n\n'
            res = front_res + res
        
        print(res)
    return 'ok'

def zipcode_to_area(zipcode):
    area = ''
    json_file = '{"100":"北市中正","103":"北市大同","104":"北市中山","105":"北市松山","106":"北市大安","108":"北市萬華","110":"北市信義","111":"北市士林","112":"北市北投","114":"北市內湖","115":"北市南港","116":"北市文山","200":"基隆市仁愛","201":"基隆市信義","202":"基隆市中正","203":"基隆市中山","204":"基隆市安樂","205":"基隆市暖暖","206":"基隆市七堵","207":"新北市萬里","208":"新北市金山","220":"新北市板橋","221":"新北市汐止","222":"新北市深坑","223":"新北市石碇","224":"新北市瑞芳","226":"新北市平溪","227":"新北市貢寮","231":"新北市新店","232":"新北市坪林","233":"新北市烏來","234":"新北市永和","235":"新北市中和","236":"新北市土城","237":"新北市三峽","238":"新北市樹林","239":"新北市鶯歌","241":"新北市三重","242":"新北市新莊","243":"新北市泰山","244":"新北市林口","247":"新北市蘆洲","248":"新北市五股","249":"新北市八里","251":"新北市淡水","252":"新北市三芝","253":"新北市石門","260":"宜蘭縣宜蘭","261":"宜蘭縣頭城","262":"宜蘭縣礁溪","263":"宜蘭縣壯圍","264":"宜蘭縣員山","265":"宜蘭縣羅東","266":"宜蘭縣三星","267":"宜蘭縣大同","268":"宜蘭縣五結","269":"宜蘭縣冬山","270":"宜蘭縣蘇澳","272":"宜蘭縣南澳","209":"連江縣南竿","210":"連江縣北竿","211":"連江縣莒光","212":"連江縣東引","300":"新竹市東區","300":"新竹市北區","300":"新竹市香山","302":"新竹縣竹北","303":"新竹縣湖口","304":"新竹縣新豐","305":"新竹縣新埔","306":"新竹縣關西","307":"新竹縣芎林","308":"新竹縣寶山","310":"新竹縣竹東","311":"新竹縣五峰","312":"新竹縣橫山","313":"新竹縣尖石","314":"新竹縣北埔","315":"新竹縣峨眉","320":"桃園市中壢","324":"桃園市平鎮","325":"桃園市龍潭","326":"桃園市楊梅","327":"桃園市新屋","328":"桃園市觀音","330":"桃園市桃園","333":"桃園市龜山","334":"桃園市八德","335":"桃園市大溪","336":"桃園市復興","337":"桃園市大園","338":"桃園市蘆竹","350":"苗栗縣竹南","351":"苗栗縣頭份","352":"苗栗縣三灣","353":"苗栗縣南庄","354":"苗栗縣獅潭","356":"苗栗縣後龍","357":"苗栗縣通霄","358":"苗栗縣苑裡","360":"苗栗縣苗栗","361":"苗栗縣造橋","362":"苗栗縣頭屋","363":"苗栗縣公館","364":"苗栗縣大湖","365":"苗栗縣泰安","366":"苗栗縣銅鑼","367":"苗栗縣三義","368":"苗栗縣西湖","369":"苗栗縣卓蘭","400":"中市中區","401":"中市東區","402":"中市南區","403":"中市西區","404":"中市北區","406":"中市北屯","407":"中市西屯","408":"中市南屯","411":"中縣太平","412":"中縣大里","413":"中縣霧峰","414":"中縣烏日","420":"中縣豐原","421":"中縣后里","422":"中縣石岡","423":"中縣東勢","424":"中縣和平","426":"中縣新社","427":"中縣潭子","428":"中縣大雅","429":"中縣神岡","432":"中縣大肚","433":"中縣沙鹿","434":"中縣龍井","435":"中縣梧棲","436":"中縣淸水","437":"中縣大甲","438":"中縣外埔","439":"中縣大安","500":"彰化縣彰化","502":"彰化縣芬園","503":"彰化縣花壇","504":"彰化縣秀水","505":"彰化縣鹿港","506":"彰化縣福興","507":"彰化縣線西","508":"彰化縣和美","509":"彰化縣伸港","510":"彰化縣員林","511":"彰化縣社頭","512":"彰化縣永靖","513":"彰化縣埔心","514":"彰化縣溪湖","515":"彰化縣大村","516":"彰化縣埔鹽","520":"彰化縣田中","521":"彰化縣北斗","522":"彰化縣田尾","523":"彰化縣埤頭","524":"彰化縣溪州","525":"彰化縣竹塘","526":"彰化縣二林","527":"彰化縣大城","528":"彰化縣芳苑","529":"彰化縣二水","540":"南投縣南投","541":"南投縣中寮","542":"南投縣草屯","544":"南投縣國姓","545":"南投縣埔里","546":"南投縣仁愛","551":"南投縣名間","552":"南投縣集集","553":"南投縣水里","555":"南投縣魚池","556":"南投縣信義","557":"南投縣竹山","558":"南投縣鹿谷","600":"嘉義市東區","600":"嘉義市西區","602":"嘉義縣番路","603":"嘉義縣梅山","604":"嘉義縣竹崎","605":"嘉義縣阿里山","606":"嘉義縣中埔","607":"嘉義縣大埔","608":"嘉義縣水上","611":"嘉義縣鹿草","612":"嘉義縣太保","613":"嘉義縣朴子","614":"嘉義縣東石","615":"嘉義縣六腳","616":"嘉義縣新港","621":"嘉義縣民雄","622":"嘉義縣大林","623":"嘉義縣溪口","624":"嘉義縣義竹","625":"嘉義縣布袋","630":"雲林縣斗南","631":"雲林縣大埤","632":"雲林縣虎尾","633":"雲林縣土庫","634":"雲林縣褒忠","635":"雲林縣東勢","636":"雲林縣臺西","637":"雲林縣崙背","638":"雲林縣麥寮","640":"雲林縣斗六","643":"雲林縣林內","646":"雲林縣古坑","647":"雲林縣莿桐","648":"雲林縣西螺","649":"雲林縣二崙","651":"雲林縣北港","652":"雲林縣水林","653":"雲林縣四湖","654":"雲林縣元長","700":"南市中西區","701":"南市東區","702":"南市南區","704":"南市北區","708":"南市安平","709":"南市安南","710":"南市永康","711":"南市歸仁","712":"南市新化","713":"南市左鎮","714":"南市玉井","715":"南市楠西","716":"南市南化","717":"南市仁德","718":"南市關廟","719":"南市龍崎","720":"南市官田","721":"南市麻豆","722":"南市佳里","723":"南市西港","724":"南市七股","725":"南市將軍","726":"南市學甲","727":"南市北門","730":"南市新營","731":"南市後壁","732":"南市白河","733":"南市東山","734":"南市六甲","735":"南市下營","736":"南市柳營","737":"南市鹽水","741":"南市善化","742":"南市大內","743":"南市山上","744":"南市新市","745":"南市安定","800":"高雄市新興","801":"高雄市前金","802":"高雄市苓雅","803":"高雄市鹽埕","804":"高雄市鼔山","805":"高雄市旗津","806":"高雄市前鎮","807":"高雄市三民","811":"高雄市楠梓","812":"高雄市小港","813":"高雄市左營","814":"高雄市仁武","815":"高雄市大社","820":"高雄市岡山","821":"高雄市路竹","822":"高雄市阿蓮","823":"高雄市田寮","824":"高雄市燕巢","825":"高雄市橋頭","826":"高雄市梓官","827":"高雄市彌陀","828":"高雄市永安","829":"高雄市湖內","830":"高雄市鳳山","831":"高雄市大寮","832":"高雄市林園","833":"高雄市鳥松","840":"高雄市大樹","842":"高雄市旗山","843":"高雄市美濃","844":"高雄市六龜","845":"高雄市內門","846":"高雄市杉林","847":"高雄市甲仙","848":"高雄市桃源","849":"高雄市那瑪夏","851":"高雄市茂林","852":"高雄市茄定","880":"澎湖縣馬公","881":"澎湖縣西嶼","882":"澎湖縣望安","883":"澎湖縣七美","884":"澎湖縣白沙","885":"澎湖縣湖西","890":"金門縣金沙","891":"金門縣金湖","892":"金門縣金寜","893":"金門縣金城","894":"金門縣烈嶼","896":"金門縣烏坵","900":"屏東縣竹田","901":"屏東縣三地門","902":"屏東縣霧臺","903":"屏東縣瑪家","904":"屏東縣九如","905":"屏東縣里港","906":"屏東縣高樹","907":"屏東縣鹽埔","908":"屏東縣長治","909":"屏東縣麟洛","911":"屏東縣竹田","912":"屏東縣內埔","913":"屏東縣萬丹","920":"屏東縣潮州","921":"屏東縣泰武","922":"屏東縣來義","923":"屏東縣萬巒","924":"屏東縣崁頂","925":"屏東縣新埤","926":"屏東縣南州","927":"屏東縣林邊","928":"屏東縣東港","929":"屏東縣珫球","931":"屏東縣佳冬","932":"屏東縣新園","940":"屏東縣枋寮","941":"屏東縣枋山","942":"屏東縣春日","943":"屏東縣獅子","944":"屏東縣車城","945":"屏東縣牡丹","946":"屏東縣恒春","947":"屏東縣滿州","950":"東縣臺東","951":"東縣綠島","952":"東縣蘭嶼","953":"東縣延平","954":"東縣卑南","955":"東縣鹿野","956":"東縣關山","957":"東縣海端","958":"東縣池上","959":"東縣東河","961":"東縣成功","962":"東縣長濱","963":"東縣太麻里","964":"東縣金峰","965":"東縣大武","966":"東縣達仁","970":"花蓮縣花蓮","971":"花蓮縣新城","972":"花蓮縣秀林","973":"花蓮縣吉安","974":"花蓮縣壽豐","975":"花蓮縣鳳林","976":"花蓮縣光復","977":"花蓮縣豐演","978":"花蓮縣瑞穗","979":"花蓮縣萬榮","981":"花蓮縣玉里","982":"花蓮縣卓溪","983":"花蓮縣富里","817":"東沙群島","819":"南沙群島","290":"釣魚臺"}'
    data = json.loads(json_file)
    try:
        area = data[str(zipcode)]
    except:
        area = -1
    # print(str(zipcode) + ' 是 ' + area)
    return area

def get_nowtime():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def logs_yellow(mess):
    print('\033[33m [' + get_nowtime() + '] ' + mess + ' \033[0m')
    return "success"

def logs_green(mess):
    print('\033[32m [' + get_nowtime() + '] ' + mess + ' \033[0m')
    return "success"

zipcode = input("請輸入郵遞區號以查詢: ")
take_mask(zipcode)