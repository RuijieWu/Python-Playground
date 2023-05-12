import requests
import json
import datetime
def GetNews():
    url = "	https://bgmlist.com/api/v1/bangumi/onair"
    weekday = datetime.date.today().weekday()
    res = requests.get(url)
    animelist = json.loads(res.text)["items"]
    News = ""
    for anime in animelist:
        time = anime["begin"][:10]
        animeweekday = datetime.date(int(time[:4]),int(time[5:7]),int(time[-2:])).weekday()
        if animeweekday==weekday:
            title = anime["title"]
            if "zh-Hans" in anime["titleTranslate"].keys():
                zhTiltle = anime["titleTranslate"]["zh-Hans"][0]
            offcialSite = anime["officialSite"]
            News += title
            News += "   "
            if "zh-Hans" in anime["titleTranslate"].keys():
                News += zhTiltle
                News += "\n"
            else:
                News+="无汉语翻译\n"
            News += offcialSite
            News +='\n'
    return News[:-1]
print(GetNews())
    #print(anime)
    #2023-04-09T08:00:00.000Z
'''
    
{'title': '機動戦士ガンダム 水星の魔女 Season2', 
'titleTranslate': {'en': ['Mobile Suit Gundam THE WITCH FROM MERCURY Season2'], 
'zh-Hans': ['机动战士高达 水星的魔女 Season2'], 
'zh-Hant': ['機動戰士鋼彈 水星的魔女 Season2', '機動戰士高達：水星的魔女 Season2']
}, 
'type': 'tv', 
'lang': 'ja', 
'officialSite': 'https://g-witch.net/', 
'begin': '2023-04-09T08:00:00.000Z', 
'broadcast': 'R/2023-04-09T08:00:00.000Z/P7D', 
'end': '', 
'comment': '', 
'sites': [
{
    'site': 'ani_one', 
    'id': 'PLC18xlbCdwtSmLNzQrV-qzNZcyKS7pMt8', 
    'begin': '2023-04-09T09:00:00.000Z', 
    'broadcast': 'R/2023-04-09T09:00:00.000Z/P7D'
}, 
{
    'site': 'ani_one_asia',
    'id': 'PLxSscENEp7JgY8RwCgV5CVcJGjCjkLkti', 
    'begin': '2023-04-09T09:00:00.000Z', 
    'broadcast': 'R/2023-04-09T09:00:00.000Z/P7D'
}, 
    {
        'site': 'bangumi', 
    'id': '403238'
    }, 
    {
    'site': 'gamer',
    'id': '130372',
    'begin': '2023-04-09T09:00:00.000Z',
    'broadcast': 'R/2023-04-09T09:00:00.000Z/P7D'
},
{
    'site': 'mytv',
    'id': 'mobilesuitgundamthewitchfrommercuryseason2_138134',
    'begin': '2023-04-09T16:00:00.000Z',
    'broadcast': 'R/2023-04-09T16:00:00.000Z/P7D'
},
{
    'site': 'viu', 
    'id': '2119357', 
    'begin': '2023-04-09T09:00:00.000Z', 
    'broadcast': 'R/2023-04-09T09:00:00.000Z/P7D'}], 
    'id': '53a79762ff2168f472fae272d332816c', 
    'pinyinTitles': ['jidongzhanshigaoda shuixingdemonv Season2', 'jdzsgd sxdmn Season2']
    }
'''
    