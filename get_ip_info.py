'''随手扒了一个获取IP信息的接口'''
import httpx

if __name__ == "__main__" :
    ip_address = input()
    image_url = f"https://zh-hans.ipshu.com/picture/{ip_address}.png"
    try:
        resp = httpx.get(image_url)
    except Exception:
        print(Exception)
    img = resp.content
    with open(f"{ip_address}.png","wb") as f:
        f.write(img)
