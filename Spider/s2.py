import pandas as pd
import time
import random
import requests
from bs4 import BeautifulSoup
from lxml import etree

# 配置信息
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
cookie = 'Bsksdjd=down_app; route=e028bf8e2ee7f213721872762d23fbc1; ASP.NET_SessionId=uyspthrqh5qlvkmcgvjxid53; sl-session=LxKtMZoXHGiDLeL19Gc88g==; Bsksdjd=down_app; Front_LoginUserKey=85EFE19FA89BC48042B0B15DFB70F3AAC1078FBF2019D8DFFA4051055F57E64A040A36A874273D6E9811D136732B8AB9933B1F99DD7D2D33DD1D2694D7713769AC9CD3994D41A2BBE518E0555C4372A1444C00DDCB87BA262252A6ACE19228EED2E5C2371A83A18269C8DC396A238D918206B6D81D58E5D09A4678F19B15A5D2CFB14D86AF82ED057C116499031335F8185D6B9DDB5C3FE289877C3C55CAE9A10AB3804BB6992771A99240E2D13B880AEAFD9DADB6C62B21543E9DCD827354CB5BA7BEA030B5ECE0'
headers = {
    'User-Agent': UserAgent,
    'Cookie': cookie
}


def generate_url(city, page):
    """动态生成正确的URL"""
    if page == 1:
        return f"https://www.muniao.com/{city}/?tn=mn19091015"
    else:
        return f"https://www.muniao.com/{city}/null-0-0-0-0-0-0-0-{page}.html?&tn=mn19091015"


def parse_item(item):
    """解析单个房源条目"""
    data = {
        '名字': item.xpath('.//a[@class="title"]/text()').get(default='无名房源').strip(),
        '价格': item.xpath('.//span[@class="price"]/text()').get(default='价格未知').strip(),
        '户型': item.xpath('.//span[@class="huxing"]/text()').get(default='').strip(),
        '可住': item.xpath('.//span[contains(@class,"guest")]/text()').get(default='').strip(),
        '评分': item.xpath('.//span[@class="score"]/text()').get(default='').strip(),
        '图片': item.xpath('.//img[@class="room-img"]/@src').get(default='')
    }
    return data


def Spider(city, page):
    try:
        url = generate_url(city, page)
        print(f"正在抓取: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        tree = etree.HTML(response.text)
        items = tree.xpath('//div[contains(@class,"room-list")]//li')  # 根据实际结构调整

        data_list = [parse_item(item) for item in items]
        df = pd.DataFrame(data_list)
        df['城市'] = city
        return df

    except Exception as e:
        print(f"抓取失败: {e}")
        return pd.DataFrame()


# 主程序
if __name__ == '__main__':
    cities = ['beijing', 'shanghai']  # 从你的HTML解析结果中获取
    all_data = pd.DataFrame()

    for city in cities:
        for page in range(1, 11):  # 假设抓取10页
            df = Spider(city, page)
            if not df.empty:
                all_data = pd.concat([all_data, df], ignore_index=True)
            time.sleep(random.uniform(1, 3))  # 随机延时

    all_data.to_csv('muniao_data.csv', index=False)
    print("数据已保存到 muniao_data.csv")