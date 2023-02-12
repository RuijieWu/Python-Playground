'''
Author: JeRyWu 1365840492@qq.com
Date: 2023-01-10 18:52:35
LastEditors: JeRyWu 1365840492@qq.com
LastEditTime: 2023-01-21 20:37:58
FilePath: \Python-Misc\B战弹幕分析.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#Easy Python Script To Anaylysis Bilibili video data
import requests
from bs4 import BeautifulSoup
import datetime
import os
import jieba
import json
from pyecharts.charts import Line
from pyecharts.charts import WordCloud

urlList = [
               
]

wordslist = {
    
}

bvList = [
    
]

def InputUrl() :
    while True : 
        print("input quit to stop")
        url = input("Input URL :") 
        if url == "quit" or url == "Quit":
             print("Done")
             break
        elif url not in urlList :
             urlList.append(url)
             
def InputBv() :
    while True : 
        print("input quit to stop")
        bv = input("Input BV number : ") 
        if bv == "quit" or bv == "Quit":
             print("Done")
             return
        elif bv not in bvList :
             bvList.append(bv)

headers = {
    "User-Agent"       : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36" ,
    #"Accept-Languages" : "zh" ,
    "Accept-Encoding"  : "utf-8"
}
'''
#Download Approach
def Download(url) :
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    with open(f"./{datetime.date.today()}.txt") as f :
        f.write(response.text)
'''
#Get Cid XML
def GetXmlByURL(url) :
    response = requests.get(url, headers=headers)
    if response.status_code == 200 :
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text,"lxml")
        content_all = soup.find_all("div")
        for content in content_all :
            if type(content) != None :
                for li in content.find_all("li") :
                    if type(li) != None :
                        if li.attrs["cid"] != None :
                                cid = soup.find("cid=(.*?)&aid=")
                                xmlUrl = f"https://comment.bilibili.com/{cid}.xml"
                                return xmlUrl
    else :
        print(f"{url} access failed")
        print(f"Status Code :{response.status_code}")
        return None
                  
def GetXmlByBV(bv) :
    url = f"https://api.bilibili.com/x/player/pagelist?bvid={bv}&jsonp=jsonp"
    res = requests.get(url)
    res.encoding = 'utf-8'
    if res.status_code == 200 :
        cid = json.loads(res.text)["data"][0]["cid"]
        xmlUrl = f"https://comment.bilibili.com/{cid}.xml"
        return xmlUrl
    else :
        print(f"{url} access failed")
        print(f"Status Code :{res.status_code}")
        return None
                        
#Analysis
def DealWords (words):
    words = jieba.lcut(words)
    for word in words :
        if word not in wordslist.keys() :
            wordslist[word] = 1
        else :
            wordslist[word] += 1
    
#ShowData
#做成词云图(jieba+pyechars)or报表（Pandas）
def ShowLine() :
    line = Line()
    line.add_xaxis( list(wordslist.keys()) )
    line.add_yaxis("词语出现次数" , list(wordslist.values()))    
    line.render(f"{datetime.date.time()}_line.html") 
    
def ShowCloud() :
    wd = WordCloud()
    wd.add(series_name = "", data_pair = wordslist.items(), word_size_range = [20,80])
    wd.render(f"{datetime.date.time()}_wordCloud.html")
    
    
if __name__ == "__main__" :
    cli = input("请选择采用1.bv号 2.URL获取目标视频数据")
    if cli == 1 :
        InputBv()
        for bv in bvList :
            xmlUrl = GetXmlByBV(bv)
            res = requests.get(xmlUrl)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text)
            for content in soup.find_all("d") :
                DealWords(content.text)
    elif cli == 2 :
        InputUrl()
        for url in urlList :
            xmlUrl = GetXmlByURL(url)
            res = requests.get(xmlUrl)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text)
            for content in soup.find_all("d") :
                DealWords(content.text)
            
    else :
        print("Input Error")
   
    ShowCloud()
    ShowLine()
        
