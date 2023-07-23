'''
Get bilibili video info and analyse it
'''
import datetime
import json
import httpx
import jieba
from bs4 import BeautifulSoup
from pyecharts.charts import Line
from pyecharts.charts import WordCloud

urlList = [
               
]

wordslist = {
    
}

bvList = [
    
]

HEADERS = {
    "User-Agent"       : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36" ,
    "Accept-Languages" : "zh" ,
    "Accept-Encoding"  : "utf-8"
}

def input_url() :
    '''recieve input info from stdio'''
    while True : 
        print("input quit to stop")
        url = input("Input URL :")
        if url == "quit" or url == "Quit":
            print("Done")
            break
        elif url not in urlList :
            urlList.append(url)

def input_bv() :
    '''recieve bv number from stdio'''
    while True : 
        print("input quit to stop")
        bv = input("Input BV number : ") 
        if bv == "quit" or bv == "Quit":
            print("Done")
            return
        elif bv not in bvList :
            bvList.append(bv)

def download(url) :
    '''download'''
    response = httpx.get(url, headers=HEADERS)
    response.encoding = 'utf-8'
    with open(f"./{datetime.date.today()}.txt",encoding='utf-8') as f :
        f.write(response.text)

def get_xml_by_url(url) :
    '''getXmlByUrl'''
    response = httpx.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,"lxml")
    content_all = soup.find_all("div")
    for content in content_all :
        if content is not None :
            for li in content.find_all("li") :
                if li is not None :
                    if li.attrs["cid"] is not None :
                            cid = soup.find("cid=(.*?)&aid=")
                            xmlUrl = f"https://comment.bilibili.com/{cid}.xml"
                            return xmlUrl

def get_xml_by_bv(bv) :
    '''getXmlByBv'''
    url = f"https://api.bilibili.com/x/player/pagelist?bvid={bv}&jsonp=jsonp"
    res = httpx.get(url)
    res.encoding = 'utf-8'
    cid = json.loads(res.text)["data"][0]["cid"]
    xmlUrl = f"https://comment.bilibili.com/{cid}.xml"
    return xmlUrl
               
#Analysis
def deal_words (words):
    '''deal words with jieba'''
    words = jieba.lcut(words)
    for word in words :
        if word not in wordslist.keys() :
            wordslist[word] = 1
        else :
            wordslist[word] += 1

def show_line() :
    '''create Line Pic to show data'''
    line = Line()
    line.add_xaxis( list(wordslist.keys()) )
    line.add_yaxis("词语出现次数" , list(wordslist.values()))    
    line.render(f"{datetime.date.time()}_line.html") 

def show_cloud() :
    '''create wordcloud Pic to show data'''
    wd = WordCloud()
    wd.add(series_name = "", data_pair = wordslist.items(), word_size_range = [20,80])
    wd.render(f"{datetime.date.time()}_wordCloud.html")

if __name__ == "__main__" :
    cli = input("请选择采用1.bv号 2.URL获取目标视频数据")
    if cli == 1 :
        input_bv()
        for bv in bvList :
            xmlUrl = get_xml_by_bv(bv)
            res = httpx.get(xmlUrl)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text)
            for content in soup.find_all("d") :
                deal_words(content.text)
    elif cli == 2 :
        input_url()
        for url in urlList :
            xmlUrl = get_xml_by_url(url)
            res = httpx.get(xmlUrl)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text)
            for content in soup.find_all("d") :
                deal_words(content.text)      
    else :
        print("Input Error")

    show_cloud()
    show_line()
