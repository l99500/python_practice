from collections import defaultdict
from send_email import send_email


class MailingList:
    """Manage groups of e-mail addresses for sending e-mails."""
    def __init__(self, data_file):
        self.email_map = defaultdict(set)
        self.data_file = data_file

    def add_to_group(self, email, group):
        self.email_map[email].add(group)

    def emails_in_groups(self, *groups):
        groups = set(groups)
        emails = set()
        for e,g in self.email_map.items():
            if g & groups:
                emails.add(e)
        return emails

    def send_mailing(self, subject, message, from_addr,
                     *groups, headers=None):
        emails = self.emails_in_groups(*groups)
        send_email(subject, message, from_addr, *emails, headers=headers)

    def save(self):
        with open(self.data_file, "w") as file:
            for email, groups in self.email_map.items():
                file.write("{}  {}\n".format(email, ",".join(groups)))

    def load(self):
        self.email_map = defaultdict(set)
        try:
            with open(self.data_file) as file:
                for line in file:
                    email, groups = line.strip().split("  ")
                    groups = set(groups.split(','))
                    self.email_map[email] = groups
        except IOError:
            pass

    """
    指向了加载和保存的方法，在下面的代码中之前保存的地址会被自动加载，结束操作之后完整的邮件列表
    会被自动保存到文件中。
    with MailingList("addresses.db") as ml:
        ml.add_to_group("friend2@example.com", "friends")
        m.send_mailing("A Party", "Friends and family only: a party", "me@example.com", \
        "friends", "family", headers=None)
    """
    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()


if __name__ == "__main__":
    m = MailingList("addresses.db")
    m.add_to_group("friend1@example.com", "friends")
    m.add_to_group("friend2@example.com", "friends")
    m.add_to_group("family1@example.com", "family")
    m.add_to_group("prol@example.com", "professional")
    # m.send_mailing("A Party", "Friends and family only: a party", "me@example.com",
    #                "friends", "family", headers=None)
    m.save()