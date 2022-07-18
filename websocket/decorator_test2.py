import socket

"""客户端"""

# 用 socket（）函数来创建套接字，socket.socket([family[, type[, proto]]])
# family: 套接字家族可以使 AF_UNIX 或者 AF_INET。
# type：套接字类型可以根据是面向连接的还是非连接分为 SOCK_STREAM 或 SOCK_DGRAM。
# protocol: 一般不填默认为 0。
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 主动初始化TCP服务器连接。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。
client.connect(('localhost', 2401))
# 接收 TCP 数据，数据以字符串形式返回，bufsize 指定要接收的最大数据量。flag 提供有关消息的其他信息，通常可以忽略。
print("Received: {0}".format(client.recv(1024)))
client.close()