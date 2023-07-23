'''
GetEveryDayNews Script
'''
import datetime
import json
import httpx
from parsel import Selector
HEADERS = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0'
        }
URL = 'https://www.zhihu.com/api/v4/columns/c_1261258401923026944/items?limit=1'
def get_url(url):
    '''Download News'''
    resp = httpx.get(url=url,headers=HEADERS)
    return resp

if __name__ == '__main__':
    data = json.loads(get_url(URL).text)["data"][0]["content"]
    content = '\n'.join(Selector(data).css('p::text').getall())
    with open(f"./{datetime.datetime.today().date()}新闻.txt","w",encoding="utf-8") as f :
        f.write(content)
