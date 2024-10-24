# Tips
编写BurpSuite的插件需要使用Python2.X的语法，因为在BurpSuite的Extender窗口中，尝试添加Python插件时，不难发现下方的提示"To Run Python Extensions,you must download the Jython standalone JAR,and configure its location in Burp Extender Options"。也就是说，我们编写的Burp插件是用Jython实现的，因此我们的Python语法不得不回退到Python2。不过对于编写简单的插件应该不会有太大的影响

# 总之照着别人写的插件抄了一份写成了Demo，就先当作先了解学习一下更深入的Burp技巧辣 :P