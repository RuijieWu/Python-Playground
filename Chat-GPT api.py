import requests
import json

while True:
    url = "https://chatgpt-api.pivotstudio.cn/prompt"
    mes = input("message:")
    res = requests.post(url,json = {
     "prompt" : mes
    })
    if res.status_code==200 :
        print(res.content.decode("utf-8"))
    else :
        print("Access failed")