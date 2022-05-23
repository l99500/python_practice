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
        self.post_param = {
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$pager",
            "__EVENTARGUMENT": 1,  # 当前页的页码
            "__VIEWSTATE": "",  # 需要从上一页的网页源码中获取
            "__VIEWSTATEGENERATOR": "56EFA5D1",
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
        with open(self.filename, 'a+', encoding="utf-8") as fw:
            # 一行有30个，构建矩阵索引
            index = list(range(0, len(info), 30))
            index.append(len(info))
            # 利用矩阵索引抽取每一行的信息
            for i in range(len(index) - 1):
                line = ",".join(info[index[i]:index[i + 1]]) + "\n"
                fw.write(line)

    def save_commerce(self, info):
        """
        这个函数是用于存储从广东能源商务网爬取的信息
        info: 用正则抽取到的信息
        """
        with open(self.filename, 'a+', encoding='utf-8') as fw:
            # 对状态和日期需要进行特殊处理，状态中提取出中文，日期区分发布日期和截止日期
            info["新状态"] = [self.extract(i, "[\u4e00-\u9fa5]+")[0] for i in info["状态"]]
            for i in range(len(info["招标号"])):
                line = info["招标号"][i] + ',' + info["招标名称"][i] + ',' + info["招标单位"][i] + ',' + \
                       info["新状态"][i] + ',' + info["方式"][i] + ',' + info["日期"][i][0] + ',' + \
                       info["日期"][i][1] + '\n'
                fw.write(line)

    def pipeline(self):
        """
        整体流程
        pattern: 正则表达式
        """
        # 第一步 获取第一页网页源代码
        first_page_code = self.download(self.url)

        # 第二步 获取网页数据的页数，并保存第一页的数据到本地文件中
        page_num_re = "页　共([0-9]+)页　记录数:26628<"
        page_num = self.extract(first_page_code, page_num_re)[0]
        print("总的页数：", page_num)
        content_re = {"招标号": "'Tender',0,'([A-Z0-9]+)'", "招标名称": '_TE_Summary">(.*)</span>',
                      "招标单位": '_TE_Company">(.*)</span>', "状态": '_GN_ST_DE">(.*)</span></span>',
                      "方式": '_lblTE_Pub">(.*)</span>', "日期": '>([-0-9]+)</td><td style="width:80px;">([-0-9]+)</td>'}
        first_page_content = self.extract(first_page_code, content_re)

        # 判断各个列的数据是否相同
        for i, j in first_page_content.items():
            if len(j) != len(first_page_content["招标号"]):
                print(i, j)
                assert False, "存在数据不全的情况"

        print(first_page_content)
        self.save_commerce(first_page_content)

        # 获取请求第二页数据的关键字信息
        self.update(first_page_code)

        # 第四步 循环获取后续的表格内容
        for i in range(1, int(page_num)):
            new_page_code = requests.post(self.url, data=self.post_param, headers=self.headers, verify=False).text
            new_page_content = self.extract(new_page_code, content_re)
            self.save_commerce(new_page_content)
            print(new_page_content)
            self.update(new_page_code, i+1)
            time.sleep(1)


if __name__ == "__main__":
    intent_url = "https://www.gdydb2b.com/Tender/ShowTenderList.aspx?type=Tender&mode=0&pre=0"
    save_file = "energy_commerce.csv"
    crawler = Crawler(intent_url, save_file)
    crawler.pipeline()
