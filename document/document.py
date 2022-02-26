class Document:
    """文件类"""

    def __init__(self):
        self.characters = []
        # 利用document类的对象来初始化cursor类
        self.cursor = Cursor(self)
        self.filename = ''

    def insert(self, character):
        if not hasattr(character, 'character'):
            # 用于检查传入的字符是Character还是str，如果是字符串则用Character进行封装
            # 这样列表中所有的对象都是Character对象了。
            character = Character(character)
        self.characters.insert(self.cursor.position, character)
        self.cursor.forward()

    def delete(self):
        del self.characters[self.cursor.position]

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(''.join(self.characters))

    @property
    def string(self):
        """给类增加一个string属性"""
        return "".join((str(c) for c in self.characters))


class Cursor:
    """如果把所有光标操作放在document一个类中，这个类会变得很庞大，
    所以最好将这些方法放在一个单独的对象中。"""

    def __init__(self, document):
        """document为文档类的对象"""
        self.document = document
        self.position = 0

    def forward(self):
        self.position += 1

    def back(self):
        self.position -= 1

    def home(self):
        while self.document.characters[self.position - 1].character != '\n':
            self.position -= 1
            if self.position == 0:
                # 回到文件的开始
                break

    def end(self):
        while self.position < len(self.document.characters) - 1 and \
                self.document.characters[self.position].character != '\n':
            self.position += 1


class Character:
    """用于表示字符"""
    def __init__(self, character, bold=False, italic=False, underline=False):
        assert len(character) == 1
        self.character = character
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def __str__(self):
        bold = "*" if self.bold else ''

        italic = "/" if self.italic else ''
        underline = "_" if self.underline else ''
        return bold + italic + underline + self.character
