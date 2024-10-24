'''
Kali上的Cewl工具的Burp插件简化版
'''
from burp import IBurpExtender
from burp import IContextMenuFactory
from java.util import ArrayList
from javax.swing import JMenuItem
from datetime import datetime
from html.parser import HTMLParser

import re

class TagStripper(HTMLParser):
    #! 提取html页面内的标签
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []
    def handle_data(self, data: str) -> None:
        self.page_text.append(data)
    def handle_comment(self, data: str) -> None:
        self.handle_data(data)
    def strip(self,html):
        self.feed(html)
        return " ".join(self.page_text)

class BurpExtender(IBurpExtender,IContextMenuFactory):
    def registerExtenderCallbacks(self,callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()
        self.wordlist = set(["password"])
        callbacks.setExtensionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)
        return
    
    def createMenuItems(self,context_menu:IContextMenuInvocation)->ArrayList():
        self.context = context_menu
        menu_list = ArrayList()
        #! 菜单的文本内容是Create Wordlist,点击后的回调wordlist_menu函数
        menu_list.add(JMenuItem("Create Wordlist",actionPerformed=self.wordlist_menu))
        return  menu_list
    
    def wordlist_menu(self,event)->None:
        http_traffic = self.context.getSelectedMessages()
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            self.hosts.add(host)
            http_response = traffic.getResponse()
            if http_response:
                self.get_words(http_response)
        
        self.display_wordlist()
        return
    
    def get_words(self,http_response)->None:
        headers , body = http_response.tostring().split('\r\n\r\n',1)
        if headers.lower().find('content-type: text') == -1:
            return
        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)
        words = re.findall("[a-zA-z]\w{2,}",page_text)
        for word in words:
            #! 太长的不要
            if len(word) <= 12:
                self.wordlist.add(word.lower())
        return
    
    def mangle(self,word)->list:
        #! 根据传入的关键词用常见后缀拓展为一系列可能的密码
        year = datetime.now().year
        #! 常见后缀
        suffixes = ["","1","!",year]
        mangled = []
        
        for password in (word,word.capitalize()):
            for suffix in suffixes:
                mangled.append("%s%s"%(password,suffixxs))
        
        return mangled
    
    def display_wordlist(self)->None:
        print("!!!comment: BHP Wordlist for site(s): %s" % ','.join(self.hosts))
        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)
        return