'''
Burp的文档讲解了如何在Burp中注册Intruder插件。插件需要有IIntruderPayloadGeneratorFactory类,
IBurpExtender主类与IIntruderPayloadGenerator类,其中IBurpExtender主类需要实现两个方法。
其一是getGeneratorName(->str),Burp会调用这个函数来获取插件的名称
其二是createNewInstance,它会返回IIntruderPayloadGenerator类的一个实例
'''
#! 编写所有插件都需要有的类
from burp import IBurpExtender

from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List,ArrayList
import random

class BurpExtender(IBurpExtender,IIntruderPayloadGeneratorFactory):
    '''拓展Burp提供的两个类'''
    def registerExtenderCallbacks(self,callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
    
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        
        return
    def getGeneratorName(self):
        return "BHP Payload Generator"
    def createNewInstance(self,attack):
        '''读取参数并返回一个拓展后的IIntruderPayloadGenerator类(类名BHPFuzzer)实例'''
        return BHPFuzzer(self,attack)
    
class BHPFuzzer(IIntruderPayloadGenerator):
    '''
    按照文档,本类需要实现三个方法
    第一个函数是hasMorePayloads,用来判定是否继续给BurpIntruder发送变异请求
    第二个函数是getNextPayload,接受所捕获的HTTP请求中的原始载荷作为参数,使原始数据变异并返回给Burp进行发送
    第三个函数是reset,一般在"预先生成了一批模糊测试数据"的情况下用到,Intruder指定载荷位置时,fuzzer可以把
    预生成的测试数据都试一遍,当前位置测试结束后Intruder会调用reset函数回到开头,等待Intruder指定下一个载荷位置
    Demo中这个第三个函数方法开摆了
    '''
    def __init__(self,extender,attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0
        
        return
    def hasMorePayloads(self):
        '''用计数器判断是否继续返回payload'''
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True
    def getNextPayload(self,current_payload):
        '''调用'''
        #! 虽然是Jython但代码也要Pythonic!
        #! current_payload是bytes类型，需要先转换
        payload = ''.join(chr(x) for x in current_payload)
        #! 调用我们自行实现的Fuzz变异器
        payload = self.mutate_payload(payload)
        self.num_iterations += 1
    def reset(self):
        '''计数器归零'''
        self.num_iterations = 0
        return

    def mutate_payload(self,original_payload):
        '''
        除此以外的代码实质上是框架,该函数是这个Demo最具有拓展价值的核心代码,负责执行Fuzz测试
        可以在这个函数中对原始Payload进行完整的自动化SQL注入测试的变异或完整的自动化XSS注入测试的变异
        由于我Burp的相关文档读的还不是很明白,以及目前所写还只是一个Demo,这个函数只做最简单的Fuzz测试即可
        :P
        '''
        picker = random.randint(1,3)
        offset = random.randint(0,len(original_payload))
        front , back = original_payload[:offset],original_payload[offset:]
        #! SQL Injection Fuzz
        if picker == 1:
            front += "'"
        #! XSS Fuzz
        elif picker ==2:
            front += "<script>alert('XSS');</script>"
        #! 随便重复原始载荷中的一段数据随机次数
        elif picker==3:
            chunk_length = random.randint(0,len(back)-1)
            repeater = random.randint(1,10)
            for _ in range(repeater):
                front += original_payload[:offset+chunk_length]
        return front + back
            