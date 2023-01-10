'''
Author: JeRyWu 1365840492@qq.com
Date: 2023-01-10 18:52:35
LastEditors: JeRyWu 1365840492@qq.com
LastEditTime: 2023-01-10 18:52:50
FilePath: \Python-Misc\B战弹幕分析.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests
from bs4 import BeautifulSoup
import datetime
import os
urlList = [
               
]

while True : 
    url = input("Input URL :") 
    if url == None :
        break
    elif url not in urlList :
        urlList.append(url)

headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}

def Download(url) :
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    for content in soup.find_all(class_ = "pic") :
        imgurl = content.find("img").attrs["src"]
        imgResponse = requests.get(imgurl,headers = headers)
        with open(".\ " + content.find("img").attrs["alt"]+".jpg","wb") as f :
            f.write(imgResponse.content)
