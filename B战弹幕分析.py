'''
ez analyze bilibili video info
'''
import datetime
import json
import httpx
import jieba
from bs4 import BeautifulSoup
from pyecharts.charts import Line
from pyecharts.charts import WordCloud

HEADERS = {
    "User-Agent"       : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36" ,
    "Accept-Encoding"  : "utf-8"
}

urlList = [

]

wordslist = {

}

bvList = [
    
]

def get_xml(bv:str) -> str:
    '''get video info xml-page'''
    url = f"https://api.bilibili.com/x/player/pagelist?bvid={bv}&jsonp=jsonp"
    try:
        res = httpx.get(url)
    except Exception:
        print(Exception)
    res.encoding = 'utf-8'
    if res.status_code == 200 :
        cid = json.loads(res.text)["data"][0]["cid"]
        xmlUrl = f"https://comment.bilibili.com/{cid}.xml"
        return xmlUrl
    else :
        print(f"{url} access failed")
        print(f"Status Code :{res.status_code}")

def deal_words (words):
    '''deal text into words by jieba'''
    words = jieba.lcut(words)
    for word in words :
        if word not in wordslist.keys() :
            wordslist[word] = 1
        else :
            wordslist[word] += 1

def show_line() :
    '''show line image'''
    line = Line()
    line.add_xaxis( list(wordslist.keys()) )
    line.add_yaxis("词语出现次数" , list(wordslist.values()))    
    line.render(f"{datetime.date.today()}_line.html") 
   
def show_cloud() :
    '''show wordcloud image'''
    wd = WordCloud()
    wd.add(series_name = "", data_pair = wordslist.items(), word_size_range = [20,80])
    wd.render(f"{datetime.date.today()}_wordCloud.html")

if __name__ == "__main__" :
    while True:
        bv = input("Input BV number or input \'q\' to stop: ") 
        if bv == "q":
            break
        if bv not in bvList :
            bvList.append(bv)

    for bv in bvList :
        xmlUrl = get_xml(bv)
        res = httpx.get(xmlUrl)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text)
        for content in soup.find_all("d") :
            deal_words(content.text)

    show_cloud()
    show_line()
