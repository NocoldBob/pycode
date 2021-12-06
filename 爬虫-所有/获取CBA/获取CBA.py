import random

import pandas as pd
import xlwt
import requests
from bs4 import BeautifulSoup

url = 'http://cbadata.sports.sohu.com/teams/team_sch/NTe003'
headers = {
    "Cookie": "IPLOC=CN5000; SUV=211206094136CEYA; gidinf=x099980109ee145e3691f94740000bca0d8b9fa5c47c; t=1638770110650",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43'
}


def getDetailInfo(url):
    print(url)
    res = requests.get(url, headers=headers).content.decode('utf-8')
    soup = BeautifulSoup(res, "lxml")
    allInfo = soup.select(".area > .cutE > div > table > tr")[1:]
    singleInfo = []
    for i in allInfo:
        title = soup.select("title")[0].string.split(':')[-1]
        time = i.contents[1].string  # 时间
        zhu = i.contents[3].string  # 主队
        score = i.contents[5].string  # 比分情况
        ke = i.contents[7].string  # 客队
        singleInfo.append([title,time,zhu,score,ke])
    return singleInfo


res = requests.get(url, headers=headers).content.decode('utf-8')
# print(res)
soup = BeautifulSoup(res, "lxml")
allList = soup.select(".area > .cutG > h2 > span > select > option")
allInfo = []
for i in allList:
    if i['value'] != '0' and i['value']:
        singleUrl = 'http://cbadata.sports.sohu.com/teams/team_sch/' + str(i['value'])
        # print(singleUrl)
        singleInfo = getDetailInfo(singleUrl)
        allInfo.extend(singleInfo)

df = pd.DataFrame(allInfo)
df.columns = ['球队名', '比赛时间', '主队', '得分情况', '客队']
df.to_csv('CBA.csv', encoding='utf_8_sig')
