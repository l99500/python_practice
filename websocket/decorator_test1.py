import socket

"""
套接字：应用程序通常通过"套接字"向网络发出请求或者应答网络请求，使主机间或者一台计算机上的进程间可以通讯。
服务器"""


def respond(client_):
    response = input("Enter a value: ")
    # 发送 TCP 数据，将 string 中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于 string 的字节大小。
    client_.send(bytes(response, 'utf8'))
    # 关闭套接字
    client_.close()


# 用 socket（）函数来创建套接字，socket.socket([family[, type[, proto]]])
# family: 套接字家族可以使 AF_UNIX 或者 AF_INET。
# type：套接字类型可以根据是面向连接的还是非连接分为 SOCK_STREAM 或 SOCK_DGRAM。
# protocol: 一般不填默认为 0。
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定地址（host,port）到套接字， 在 AF_INET下，以元组（host,port）的形式表示地址。
server.bind(('localhost', 2401))
# 开始 TCP 监听。backlog 指定在拒绝连接之前，操作系统可以挂起的最大连接数量。
# 该值至少为 1，大部分应用程序设为 5 就可以了。
server.listen(1)

try:
    while True:
        # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
        client, addr = server.accept()
        respond(client)
finally:
    # 关闭套接字
    server.close()