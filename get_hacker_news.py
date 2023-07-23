'''
GetHackerNews Script
'''
import httpx
from lxml import etree

HEADERS = {
    "User-Agent"       : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36" ,
    "Accept-Languages" : "zh" ,
    "Accept-Encoding"  : "utf-8"
}
for page in range(1,2):
    url = f'http://hackernews.cc/page/{page}'
    r = httpx.get(url,headers=HEADERS).text
    news = ""
    tree = etree.HTML(r)
    title = tree.xpath('//h3[@class="classic-list-title"]/a/text()')
    href = tree.xpath('//h3[@class="classic-list-title"]/a/@href')
    for num in range(1,len(title)):
        news +=f"{title[num]}\n{href[num]}\n"
    print(news)


