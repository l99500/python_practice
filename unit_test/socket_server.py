import socket

"""
在一个单独的进程中运行一个服务器，
然后多个测试与其建立连接。
"""

# 用 socket（）函数来创建套接字，socket.socket([family[, type[, proto]]])
# family: 套接字家族可以使 AF_UNIX 或者 AF_INET。
# type：套接字类型可以根据是面向连接的还是非连接分为 SOCK_STREAM 或 SOCK_DGRAM。
# protocol: 一般不填默认为 0。
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# setsockopt(level,optname,value)
# level定义了哪个选项将被使用。通常情况下是SOL_SOCKET，意思是正在使用的socket选项。
# S.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# 这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，
# 否则操作系统会保留几分钟该端口。
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定地址（host,port）到套接字， 在 AF_INET下，以元组（host,port）的形式表示地址。
s.bind(('localhost', 1028))

# 开始 TCP 监听。backlog 指定在拒绝连接之前，操作系统可以挂起的最大连接数量。
# 该值至少为 1，大部分应用程序设为 5 就可以了。
s.listen(1)

while True:
    # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
    client, address = s.accept()
    data = client.recv(1024)
    # 将输入值原路返回
    client.send(data)
    # 关闭套接字
    client.close()

