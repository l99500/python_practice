import requests
import re
import time

"""
爬取aspx网站，翻页url不变
"""


class Crawler:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.138 Safari/537.36'}
        # 需要根据自己的网页进行修改
        self.post_param = {
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$pager",
            "__EVENTARGUMENT": 1,  # 当前页的页码
            "__VIEWSTATE": "",  # 需要从上一页的网页源码中获取
            "__VIEWSTATEGENERATOR": "43D0C51D",
            "__VIEWSTATEENCRYPTED": "",  # 默认为空
            "__EVENTVALIDATION": "",  # 从上一页的网页源码中获取
            "KeyWord": " 输入招标名称进行搜索",
            "ctl00$ContentPlaceHolder1$pager_input": 1  # 上一页的页码
        }

    def download(self, url):
        """
        根据传入的url信息下载网页源码
        url：网页链接
        """
        r = requests.get(url, headers=self.headers, verify=False)
        return r.text

    @staticmethod
    def extract(content, pattern):
        """
        利用正则表达式从网页源码中提取感兴趣的内容
        content: 网页源码
        pattern: 正则表达式(单条字符串或者多条构成的字典)
        """
        if isinstance(pattern, dict):
            # 如果是字典
            result = {}
            for i, j in pattern.items():
                result[i] = re.findall(j, content)
        else:
            result = re.findall(pattern, content)
        return result

    def update(self, info, page_num=1):
        """
        更新关键字字典，用于请求下一页数据的参数
        info：上一页的源码
        page_num: 上一页的页码
        """
        view_state = self.extract(info, '"__VIEWSTATE".value="(.*)" />')[0]
        self.post_param["__VIEWSTATE"] = view_state
        event_validation = self.extract(info, '"__EVENTVALIDATION" value="(.*)" />')[0]
        self.post_param["__EVENTVALIDATION"] = event_validation
        self.post_param["ctl00$ContentPlaceHolder1$pager_input"] = page_num
        self.post_param["__EVENTARGUMENT"] = page_num + 1

    def save(self, info):
        """
        将爬取的信息保存到本地文件, "a+":在原有文件上追加信息
        info：爬取到的信息
        """
        # 去除抽取信息中的第一个元素，这个不是需要的信息
        if info[0] == "Request Reason":
            info = info[1:]
        # 校验抽取到的信息数量是否能被30整除
        assert len(info) % 30 == 0, "抽取信息数量不对，不能被30整除"
        print("当前页数信息：", info)
        with open(self.filename, 'a+', encoding="utf-8") as fw:
            # 一行有30个，构建矩阵索引
            index = list(range(0, len(info), 30))
            index.append(len(info))
            # 利用矩阵索引抽取每一行的信息
            for i in range(len(index) - 1):
                line = ",".join(info[index[i]:index[i + 1]]) + "\n"
                fw.write(line)

    def pipeline(self):
        """
        整体流程
        pattern: 正则表达式
        """
        # 第一步 获取第一页网页源代码
        first_page_code = self.download(self.url)

        # 第二步 获取网页数据的页数，并保存第一页的数据到本地文件中
        page_num_re = "Input Page 0 - ([0-9]+)"
        page_num = self.extract(first_page_code, page_num_re)
        page_num = page_num[0]
        print("总的页数：", page_num)
        content_re = '<td align="center">(.{0,50}?)</td>'
        first_page_content = self.extract(first_page_code, content_re)

        print(first_page_content)
        self.save(first_page_content)

        # 获取请求第二页数据的关键字信息
        self.update(first_page_code)

        # 第四步 循环获取后续的表格内容
        for i in range(1, int(page_num)):
            print("当前页数：", i+1)
            new_page_code = requests.post(self.url, data=self.post_param, headers=self.headers, verify=False).text
            new_page_content = self.extract(new_page_code, content_re)
            self.save(new_page_content)
            self.update(new_page_code, i+1)
            # 每爬取一页，休息1秒，防止服务器中断请求
            time.sleep(1)


if __name__ == "__main__":
    intent_url = "https://www.gdydb2b.com/Tender/ShowTenderList.aspx?type=Tender&mode=0&pre=0"
    save_file = "energy_commerce.csv"
    crawler = Crawler(intent_url, save_file)
    crawler.pipeline()
