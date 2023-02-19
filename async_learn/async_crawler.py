import asyncio
import aiohttp
import requests
import time

"""
协程的主要用途在IO密集型场景
"""


def download_img(url):
    file_name = url.rsplit('/')[-1]
    print(f"下载图片: {file_name}")
    response = requests.get(url)
    with open(file_name, mode='wb') as file:
        file.write(response.content)
    print(f"下载完成：{file_name}")


def syn_main():
    urls = [
        "https://tenfei05.cfp.cn/creative/vcg/800/new/VCG41560336195.jpg",
        "https://alifei01.cfp.cn/creative/vcg/800/new/VCG41N1448097401.jpg",
        "https://tenfei04.cfp.cn/creative/vcg/800/new/VCG41N1446140505.jpg"
    ]
    for item in urls:
        download_img(item)


async def download_img_async(session, url):
    file_name = url.rsplit('/')[-1]
    print(f"下载图片: {file_name}")
    response = await session.get(url, ssl=False)
    content = await response.content.read()
    with open(file_name, mode='wb') as file:
        file.write(content)
    print(f"下载完成：{file_name}")


async def async_main():
    urls = [
        "https://tenfei05.cfp.cn/creative/vcg/800/new/VCG41560336195.jpg",
        "https://alifei01.cfp.cn/creative/vcg/800/new/VCG41N1448097401.jpg",
        "https://tenfei04.cfp.cn/creative/vcg/800/new/VCG41N1446140505.jpg"
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(download_img_async(session, url)) for url in urls]
        await asyncio.wait(tasks)


if __name__ == "__main__":
    t1 = time.time()
    # 使用同步方式下载图片
    syn_main()
    t2 = time.time()
    print(f"同步方式下载耗时：{t2 - t1}")
    # 使用异步方式下载图片
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
    t3 = time.time()
    print(f"异步方式下载耗时：{t3 - t2}")
