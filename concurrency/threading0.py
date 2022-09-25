from threading import Thread


class InputReader(Thread):
    """构造一个线程，所有代码都在一个新线程中运行"""
    def run(self):
        """线程暂停等待键盘的输入"""
        self.line_of_text = input()


print("Enter some text and press enter: ")
thread = InputReader()
# 开始运行新线程
thread.start()

# # 如果这里使用thread.run(), 线程不会被激活，只是一直等待输入
# thread.run()

count = result = 1
# 新线程等待输入时，初始线程继续执行循环中的平方计算，直到run方法退出
while thread.is_alive():
    result = count * count
    count += 1

print("calculated squares up to {0} * {0} = {1}".format(count, result))
print("while you typed '{}'".format(thread.line_of_text))

