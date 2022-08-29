import xlrd
from urllib.parse import quote
import requests
import pandas as pd

data = xlrd.open_workbook(r'./data.xls')
table = data.sheets()[0]

tables = []
tables_raw = []
def import_excel(excel):
    for rown in range(1,excel.nrows):
        array1 = {'year': '', 'university': '', 'major': '','score':''}
        array1['year'] = str(int(table.cell_value(rown, 0)))
        array1['university'] = table.cell_value(rown, 1)  # 将中文转为urlencode
        array1['major'] = table.cell_value(rown, 2)
        tables_raw.append(array1)
        array2 = {'year':'','university':'','major':''}
        array2['year'] = str(int(table.cell_value(rown,0)))
        array2['university'] = quote(table.cell_value(rown,1)) #将中文转为urlencode
        array2['major'] = quote(table.cell_value(rown,2))
        tables.append(array2)

urls = []
def weburl(tables): #拼接爬虫链接
    url = 'https://common-mini.okaoyan.com/api/kaoyanpai/select-score?'
    for i in tables:
        array = url + 'year=' + i['year'] + '&university=' + i['university'] + '&major=' + i['major']
        urls.append(array)

headers = {
    'Host':'common-mini.okaoyan.com',
    'Connection':'keep-alive',
    'X-Tag':'flyio',
    'content-type':'application/x-www-form-urlencoded',
    'Authorization':'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxLDEyOTMzNjYgMTY1MDM1OTUwMjUzMCJ9.7_IMMXZJUkXYYLbAIBDwkr9_vmDnSa5VoVG8cHQ7aBA',
    'Accept-Encoding':'gzip,compress,br,deflate',
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x1800142b) NetType/WIFI Language/zh_CN',
    'Referer':'https://servicewechat.com/wxfc0db1971197c626/61/page-frame.html'
}

def get_message(urls):
    lenth = len(urls)
    for i in range(lenth):
        response = requests.get(url=urls[i],headers=headers)
        find_score(response.json(),i)


def find_score(info_raw,index):
    score = '500'
    info = info_raw['rows']
    for i in info:
        if i['firstTry'] < score:
            score = i['firstTry']
    if score == '500':
        score = '0'
    tables_raw[index]['score'] = score

if __name__ == '__main__':
    import_excel(table)
    weburl(tables)
    '''
    print(type(tables))
    for i in tables:
        print(i)
    for j in urls:
        print(j) 
    '''
    get_message(urls)
    for i in tables_raw:
        print(i)
    final_data = pd.DataFrame(data=tables_raw)
    final_data.to_excel('./final_data.xlsx',encoding='utf-8')