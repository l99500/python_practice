import smtplib
from email.mime.text import MIMEText

"""
http服务器拥有内置的简单邮件传输协议SMTP服务器，可以捕获所有发送的信息而不会真的发出去
启动服务器的命令：
python -m smtpd -n -c DebuggingServer localhost:1025
命令行中这条指令会启动一个SMTP服务器，运行在本地1025端口，
启用DebuggingServer类，不会真的发送邮件给目的地址，而是接收到信息时打印到终端屏幕。

——————————————————————————————————
本函数文件为发送邮件的代码
"""


def send_email(subject, message, from_addr, *to_addrs, host="localhost",
               port=1025, headers=None):
    headers = {} if headers is None else headers
    email = MIMEText(message)
    email['Subject'] = subject
    email['From'] = from_addr
    for header, value in headers.items():
        email[headers] = value

    sender = smtplib.SMTP(host, port)
    for addr in to_addrs:
        del email['To']
        email['To'] = addr
        sender.sendmail(from_addr, addr, email.as_string())
    sender.quit()


if __name__ == "__main__":
    send_email("A model subject", "The message contents", "from@example.com",
               "to1$example.com", "to2@example.com")