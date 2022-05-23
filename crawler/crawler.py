import requests
import re


class Crawler:
    """
    爬虫类
    """
    def __init__(self, filename):
        """
        类初始化
        filename: 保存文件的路径
        """
        self.filename = filename
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.138 Safari/537.36',}

    def download(self, url):
        """
        根据传入的url信息下载网页源码
        url：网页链接
        """
        r = requests.get(url, headers=self.headers)
        return r.text

    @staticmethod
    def extract(content, pattern):
        """
        利用正则表达式从网页源码中提取感兴趣的内容
        content: 网页源码
        pattern: 正则表达式
        """
        result = re.findall(pattern, content)
        return result

    def save(self, info):
        """
        将爬取的信息保存到本地文件, "a+":在原有文件上追加信息
        info：爬取到的信息
        """
        with open(self.filename, 'a+', encoding="utf-8") as fw:
            # 一行有30个，构建矩阵索引
            index = list(range(0, len(info), 30))
            index.append(len(info))
            # 利用矩阵索引抽取每一行的信息
            for i in range(len(index)-1):
                line = ",".join(info[index[i]:index[i+1]]) + "\n"
                fw.writelines(line)

    def crawler_from_file(self, file_path, pattern):
        """
        从已下载网页源码中提取信息
        file_path: 源码文件保存路径
        """
        # 将网页源码读入计算机
        url_info = open(file_path, "r", encoding="utf-8").read()
        # 从源码中提取表头
        excel_header = self.extract(url_info, pattern[0])
        # 将提取信息中的空格去处
        excel_header = [i.replace(" ", "") for i in excel_header]
        print(excel_header)
        # 从源码中提取表格中的信息
        excel_info = self.extract(url_info, pattern[1])[1:]
        print(excel_info[299])
        # 将抽取到的信息保存到文件
        self.save(excel_info)


if __name__ == '__main__':
    # 从保存的源码中提取信息
    # 网页源码文件路径
    web_file_path = "D:/practice/sanic/crawler/网页源代码.txt"
    # 从类初始化对象
    crawler = Crawler("crawler.csv")
    header_pattern = '<td class="Title" width="150">\n(.+)</td>'
    content_pattern = '<td align="center">(.{0,50}?)</td>'
    crawler.crawler_from_file(web_file_path, [header_pattern, content_pattern])
