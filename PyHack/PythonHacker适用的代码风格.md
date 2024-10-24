PythonHacker适用的代码风格与大部分Python程序开发时所应具备的代码风格是类似的，例如

    from AAA import AA
    from BBB import BB
    import A
    import B

    def func():

    class Object(object):

    if __name__ == "__main__":

或者

    from AAA import AA
    from BBB import BB
    import A
    import B

    def func():

    class Object(object):

    def main():

    if __name__ == "__main__":
        main()

注意，最好不要为了图方便使用From XXX import *这样的导入方式，这会使代码变得臃肿，同时容易引起冲突和不必要的麻烦。在导入库的时候最好按照字符顺序进行导入，这样可以为检查哪些包没有导入或是否重复导入提供方便。这个程序运行的代码应该写入if __name__ == "__main__"后，这样便于该程序的复用

但与标准的Python程序开发不同的是，我们在编写脚本的时候代码可以|"脏"一些，比起代码风格的美与否，我们更关注它是否便捷简易而实用。