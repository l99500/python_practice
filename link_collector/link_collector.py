from urllib.request import urlopen
from urllib.parse import urlparse
import re
import sys

"""
运行步骤：
1. cd case_study_serve
2. python -m http.server
3. cd ..
4. python link_collector.py http://localhost:8000/case_study_serve/
"""

# 生成正则表达式对象
LINK_REGEX = re.compile("<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>")


class LinkCollector:
    def __init__(self, url):
        """
        提取主机名
        url: http://localhost:8000/case_study_serve/
        result: http://localhost:8000/
        """
        self.url = "http://" + urlparse(url).netloc
        self.collected_links = set()
        self.visited_links = set()

    def collect_links(self, path="/"):
        full_url = self.url + path
        self.visited_links.add(full_url)

        page = str(urlopen(full_url).read())
        links = LINK_REGEX.findall(page)
        print(links)
        links = {self.normalize_url(path, link) for link in links}
        self.collected_links = links.union(self.collected_links)
        unvisited_links = links.difference(self.visited_links)

        for link in unvisited_links:
            if link.startswith(self.url):
                self.collect_links(urlparse(link).path)

    def normalize_url(self, path, link):
        """
        将所有链接统一改成完整的url，包括主机名和相对路径
        """
        if link.startswith("http://"):
            return link
        elif link.startswith("/"):
            return self.url + link
        else:
            return self.url + path.rpartition('/')[0] + '/' + link


if __name__ == "__main__":
    collector = LinkCollector(sys.argv[1])
    collector.collect_links()
    for link_ in collector.collected_links:
        print(link_)