'''
Get CTF Matches info
'''
import json
import requests

URL = "http://event.ctf.probius.xyz/cn_CTF"
if __name__ == "__main__":
    try:
        resp = requests.get(url)
    except Exception:
        print(Exception)
    matches = json.loads(resp.text)
    for match in matches[1:]:
        print(match)
