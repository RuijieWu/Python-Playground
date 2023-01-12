'''
Author: JeRyWu 1365840492@qq.com
Date: 2023-01-12 17:33:19
LastEditors: JeRyWu 1365840492@qq.com
LastEditTime: 2023-01-12 17:33:22
FilePath: \Python-Misc\获取每日新闻.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests,json
from parsel import Selector
import datetime

def getUrl(url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0'}
    response = requests.get(url=url,headers=headers)
    return response
if __name__ == '__main__':
    url = 'https://www.zhihu.com/api/v4/columns/c_1261258401923026944/items?limit=1'
    data = json.loads(getUrl(url).text)["data"][0]["content"]
    content = '\n'.join(Selector(data).css('p::text').getall())
    with open(f"./{datetime.datetime.today().date()}新闻.txt","w") as f :
        f.write(content)