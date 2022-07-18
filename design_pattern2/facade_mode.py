"""
门面模式：
1、用于为复杂系统提供简单的借口，定义一个对象来概括系统的特有用途。
3、门面在很多方面和适配器很像，主要区别在于门面模式试图从复杂接口中抽象出一个简化版泵。
因为不太了解邮件的发送，下面的代码未进行测试。
"""

import smtplib
import imaplib


class EmailFacade:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, message):
        """发邮件"""
        if not "@" in self.username:
            from_email = "{0}@{1}".format(self.username, self.host)
        else:
            from_email = self.username

        message = (
            "From: {0}\r\n"
            "To: {1}\r\n"
            "Subject: {2}\r\n\r\n{3}"
        ).format(from_email, to_email, subject, message)

        smtp = smtplib.SMTP(self.host)
        smtp.login(self.username, self.password)
        smtp.sendmail(from_email, [to_email], message)

    def get_inbox(self):
        mailbox = imaplib.IMAP4(self.host)
        mailbox.login(bytes(self.username, "utf8"), bytes(self.password, "utf8"))
        mailbox.select()
        x, data = mailbox.seach(None, "ALL")
        messages = []
        for num in data[0].split():
            x, message = mailbox.fetch(num, '(RFC822)')
            messages.append(message[0][1])
        return messages
