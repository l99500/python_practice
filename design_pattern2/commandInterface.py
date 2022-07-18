import sys

"""
命令模式：
命令模式在需要执行的操作和对象之间添加新的抽象层，通常是在事后完成的。
定义一些触发类，用来模拟工具条、菜单以及键盘事件等，它们也不会真的涉及这些操作，
我们可以看到它们是如何与命令、接收者以及客户端代码解耦的。
"""


class Window:
    def exit(self):
        sys.exit(0)


class Document:
    def __init__(self, filename):
        self.filename = filename
        self.contents = "This file cannot be modified"

    def save(self):
        with open(self.filename, 'w') as file:
            file.write(self.contents)


class ToolbarButton:
    """command属性在执行的时候再赋予，下面的类也一样"""
    def __init__(self, name, iconname):
        self.name = name
        self.iconname = iconname

    def click(self):
        self.command.execute()


class MenuItem:
    def __init__(self, menu_name, menuitem_name):
        self.menu = menu_name
        self.item = menuitem_name

    def click(self):
        self.command.execute()


class KeyboardShortcut:
    def __init__(self, key, modifier):
        self.key = key
        self.modifier = modifier

    def keypress(self):
        self.command.execute()


class SaveCommand:
    def __init__(self, document):
        self.document = document

    def execute(self):
        self.document.save()


class ExitCommand:
    def __init__(self, window):
        self.window = window


def execute(self):
    self.window.exit()


if __name__ == "__main__":
    window = Window()
    document = Document("a_document.txt")
    save = SaveCommand(document)
    exit = ExitCommand(window)

    save_button = ToolbarButton('save', "save.png")
    save_button.command = save
    save_keystroke = KeyboardShortcut("s", "ctrl")
    save_keystroke.command = save
    exit_menu = MenuItem("File", "Exit")
    exit_menu.command = exit