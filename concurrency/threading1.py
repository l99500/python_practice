from threading import Thread
import json
import requests
import time

CITIES = [
    '长沙', '珠海', '北京', '广州',
    "合肥", '贵阳', '上海', '苏州',
    '拉萨', '杭州'
]


class TempGetter(Thread):
    def __init__(self, city):
        # 我们在一个线程中构造的数据可以被其他正在运行的线程所访问
        super().__init__()
        self.city = city
        self.weather_api = 'https://api.seniverse.com/v3/weather/now.json'
        self.api_key = '****'  # 心知天气秘钥
        self.city = city
        self.language = 'zh-Hans'
        self.unit = 'c'
        self.request_session = requests.session()
        self.request_session.keep_alive = False

    def run(self):
        result = self.request_session.get(self.weather_api, params={
            'key': self.api_key,
            'location': self.city,
            'language': self.language,
            'unit': self.unit
        }, timeout=1)
        result = json.loads(result.text)
        print(result)
        return result


threads = [TempGetter(c) for c in CITIES]
start = time.time()
for thread in threads:
    thread.start()

for thread in threads:
    # 等这个线程执行完毕再做其他事
    thread.join()

# for thread in threads:
#     print(thread)

print("Got {} temps in {} seconds".format(len(threads), time.time() - start))