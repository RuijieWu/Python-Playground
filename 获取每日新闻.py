'''
Get 60s Daily News
'''
import datetime
import json
from parsel import Selector
import httpx

HEADERS = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0'}
URL = 'https://www.zhihu.com/api/v4/columns/c_1261258401923026944/items?limit=1'

if __name__ == '__main__':
    try:
        resp = httpx.get(URL,headers=HEADERS)
    except Exception:
        print(Exception)
    data = json.loads(resp.text)["data"][0]["content"]
    content = '\n'.join(Selector(data).css('p::text').getall())
    with open(f"./{datetime.datetime.today().date()}新闻.txt","w",encoding='utf-8') as f :
        f.write(content)
