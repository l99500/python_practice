import re
import sys
import json
from pathlib import Path

# 这里使用r，则不需要转移反斜杠（原生字符串）
DIRECTIVE_RE = re.compile(
    r'/\*\*\s*(include|variable|loopover|endloop|loopvar)'
    r'\s*([^ *]*)\s*\*\*/'
)


class TemplateEngine:
    def __init__(self, in_filename, out_filename, context_filename):
        self.template = open(in_filename).read()
        self.working_dir = Path(in_filename).absolute().parent
        self.pos = 0
        self.out_file = open(out_filename, 'w')
        with open(context_filename) as context_file:
            self.context = json.load(context_file)

    def process(self):
        # 首先找到第一个匹配正则表达式的字符串
        match = DIRECTIVE_RE.search(self.template, pos=self.pos)  # pos 匹配的起始位置
        while match:
            # 输出从开始到匹配开始位置的字符串
            self.out_file.write(self.template[self.pos:match.start()])
            directive, argument = match.groups()
            # 将指令名转换为方法名
            method_name = "process_{}".format(directive)
            # 从类中取出同名方法，并传入参数
            getattr(self, method_name)(match, argument)
            match = DIRECTIVE_RE.search(self.template, pos=self.pos)
        # 将剩余内容写入输出文件
        self.out_file.write(self.template[self.pos:])

    def process_include(self, match, argument):
        """查找引入的文件病插入文件内容"""
        with (self.working_dir / argument).open() as include_file:
            self.out_file.write(include_file.read())
            self.pos = match.end()

    def process_variable(self, match, argument):
        """查找变量并插入"""
        self.out_file.write(self.context.get(argument, ''))
        self.pos = match.end()

    def process_loopover(self, match, argument):
        """当遇到loopover指令时初始化三个变量"""
        self.loop_index = 0
        self.loop_list = self.context.get(argument, [])
        self.pos = self.loop_pos = match.end()

    def process_loopvar(self, match, argument):
        """输出loop_list变量当前位置的值，然后跳到指令的尾部"""
        self.out_file.write(self.loop_list[self.loop_index])
        self.pos = match.end()

    def process_endloop(self, match, argument):
        """用于确定是否已经遍历玩了loop_list"""
        self.loop_index += 1
        if self.loop_index >= len(self.loop_list):
            self.pos = match.end()

            del self.loop_index
            del self.loop_list
            del self.loop_pos
        else:
            self.pos = self.loop_pos


if __name__ == '__main__':
    # 从命令行读取参数
    # in_filename_, out_filename_, context_filename_ = sys.argv[1:]
    in_filename_ = '../regexp_parse/case_study_input/main.html'
    out_filename_ = 'result.txt'
    context_filename_ = '../regexp_parse/case_study_input/context.json'
    engine = TemplateEngine(in_filename_, out_filename_, context_filename_)
    engine.process()