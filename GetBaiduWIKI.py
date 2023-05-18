import requests
import json

url = "http://baike.baidu.com/api/openapi/BaikeLemmaCardApi"
key = input("Key:")
params = {
    "scope":103,
    "format":"json",
    "appid":379020,
    "bk_key":key,
    "bk_length":600
}
res = requests.get(url,params=params)
if res.status_code == 200:
    data = json.loads(res.text)
    title = data["title"]
    desc = data["desc"]
    card = data["card"]
    print(title,"   ",desc)
    for info in card:
        print(info["name"],"   ",info["value"][0])
    image_url = data["image"]
    abstrcat = data["abstract"]
    bk_page = data["url"]
    print(image_url)
    print(abstrcat)
    print(bk_page)
    
    