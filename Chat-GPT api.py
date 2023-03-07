import requests
import json
import time
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Connection':'close'
    }
while True:
    url = "https://chatgpt-backend.pivotstudio.cn/api/prompt"
    mes = input("message:")
    if mes == "exit":
        break
    else:
        res = requests.post(url,headers = headers,json = {
        "prompt" : mes
        })
        if res.status_code==200 :
            res.encoding="utf-8"
           # text = res.content.decode("utf-8")
            text = res.text
            print(text)
        else:
            print(f"{res.status_code} Access failed")
        sleep(1)
    