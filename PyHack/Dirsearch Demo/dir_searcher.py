'''
Ez dir_searcher
'''
import queue
import sys
import threading
import httpx
import config

def get_words(resume=None)->queue.Queue:
    '''open wordlist file and create a queue according it '''
    def extend_words(word)->None:
        '''添加扫描路径队列'''
        if '.' in word:
            words.put(f"/{word}")
        else:
            words.put(f"/{word}/")
        
        for extension in config.EXTENSIONS:
            words.put(f"/{word}{extension}")

    with open(config.WORDLIST) as fp:
        raw_words = fp.read()
    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        #! 从传入的上次扫描中断的位置(resume)继续
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f"Resuming wordlist from {resume}")
        else:
            print(word)
            extend_words(word)
        return words

def dir_search(words):
    '''send request to test'''
    while not words.empty():
        url = f"{config.TARGET}{words.get()}"
        try:
            resp = httpx.get(url,headers=config.HEADERS)
        except httpx._exceptions.ConnectError:
            sys.stderr.write('x')
            sys.stderr.flush()
            continue
        if resp.status_code == 200:
            print(f"\nSuccess {resp.status_code} {url}")
        elif resp.status_code == 404:
            sys.stderr.write('.')
            sys.stderr.flush()
        else:
            print(f"{resp.status_code} {url}")

if __name__ == "__main__":
    words = get_words
    for _ in range(config.THREADS):
        thread = threading.Thread(target=dir_search,args=(words,))
        thread.start()
            