# Title: wechat push CVE-2020
# Date: 2020-5-9
# Exploit Author: weixiao9188
# Version: 4.0
# Tested on: Linux,windows
# coding:UTF-8
import requests
import json
import time
import urllib3
import os
import pandas as pd

time_sleep = 20 # 每隔20秒爬取一次
while(True):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"}
    # 判断文件是否存在
    datas = []
    response1 = None
    response2 = None
    if os.path.exists("olddata.csv"):
        # 如果文件存在则每次爬取10个
        df = pd.read_csv("olddata.csv", header=None)
        datas = df.where(df.notnull(),None).values.tolist()# 将提取出来的数据中的nan转化为None
        requests.packages.urllib3.disable_warnings()
        response1 = requests.get(url="https://api.github.com/search/repositories?q=CVE-2021&sort=updated&per_page=10",
                                 headers=headers,verify=False)
        response2 = requests.get(url="https://api.github.com/search/repositories?q=RCE&ssort=updated&per_page=10",
                                 headers=headers,verify=False)

    else:
        # 不存在爬取全部
        datas = []
        requests.packages.urllib3.disable_warnings()
        response1 = requests.get(url="https://api.github.com/search/repositories?q=CVE-2021&sort=updated&order=desc",headers=headers,verify=False)
        response2 = requests.get(url="https://api.github.com/search/repositories?q=RCE&ssort=updated&order=desc",headers=headers,verify=False)

    data1 = json.loads(response1.text)
    data2 = json.loads(response2.text)
    for j in [data1["items"],data2["items"]]:
        for i in j:
            s = {"name":i['name'],"html":i['html_url'],"description":i['description']}
            s1 =[i['name'],i['html_url'],i['description']]
            if s1 not in datas:
                #print(s1)
                #print(datas)
                params = {
                     "text":s["name"],
                    "desp":" 链接:"+str(s["html"])+"\n简介"+str(s["description"])
                }
                print("当前推送为"+str(s)+"\n")
                print(params)
                requests.packages.urllib3.disable_warnings()
                requests.get("https://sctapi.ftqq.com/SCT68513T20RxXKZZlL1mtwHtu8UtTyPQ.send",params=params,timeout=10,verify=False)
                #time.sleep(1)#以防推送太猛
                print("推送完成!")
                datas.append(s1)
            else:
                pass
                #print("数据已存在!")
    pd.DataFrame(datas).to_csv("olddata.csv",header=None,index=None)
    time.sleep(time_sleep)
