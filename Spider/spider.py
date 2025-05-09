#https://www.muniao.com/beijing/?tn=mn19091015
#https://www.muniao.com/beijing/null-0-0-0-0-0-0-0-1.html?&tn=mn19091015#第一页
#https://www.muniao.com/beijing/null-0-0-0-0-0-0-0-2.html?start_date=2025-05-07&end_date=2025-05-08&tn=mn19091015
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
html ="""<ul class="s_citywindow_main" style="display: block;">
                                    <li data-path="beijing" data-url="bj" data-city="北京"><a href="javascript:void(0)">北京</a></li>
                                    <li data-path="shanghai" data-url="sh" data-city="上海"><a href="javascript:void(0)">上海</a></li>
                                    <li data-path="qinhuangdao" data-url="qhd" data-city="秦皇岛"><a href="javascript:void(0)">秦皇岛</a></li>
                                    <li data-path="qingdao" data-url="qingdao" data-city="青岛"><a href="javascript:void(0)">青岛</a></li>
                                    <li data-path="xiamen" data-url="xm" data-city="厦门"><a href="javascript:void(0)">厦门</a></li>
                                    <li data-path="chengdu" data-url="chengdu" data-city="成都"><a href="javascript:void(0)">成都</a></li>
                                    <li data-path="hangzhou" data-url="hz" data-city="杭州"><a href="javascript:void(0)">杭州</a></li>
                                    <li data-path="dalian" data-url="dalian" data-city="大连"><a href="javascript:void(0)">大连</a></li>
                                    <li data-path="chongqing" data-url="cq" data-city="重庆"><a href="javascript:void(0)">重庆</a></li>
                                    <li data-path="guangzhou" data-url="gz" data-city="广州"><a href="javascript:void(0)">广州</a></li>
                                    <li data-path="nanjing" data-url="nj" data-city="南京"><a href="javascript:void(0)">南京</a></li>
                                    <li data-path="xian" data-url="xa" data-city="西安"><a href="javascript:void(0)">西安</a></li>
                                    <li data-path="sanya" data-url="sy" data-city="三亚"><a href="javascript:void(0)">三亚</a></li>
                                    <li data-path="shenzhen" data-url="shenzhen" data-city="深圳"><a href="javascript:void(0)">深圳</a></li>
                                    <li data-path="weihai" data-url="zz" data-city="威海"><a href="javascript:void(0)">威海</a></li>
                                    <li data-path="wuhan" data-url="wh" data-city="武汉"><a href="javascript:void(0)">武汉</a></li>
                                    <li data-path="yantai" data-url="zz" data-city="烟台"><a href="javascript:void(0)">烟台</a></li>
                                    <li data-path="suzhou" data-url="sz" data-city="苏州"><a href="javascript:void(0)">苏州</a></li>
                                    <li data-path="tianjin" data-url="tj" data-city="天津"><a href="javascript:void(0)">天津</a></li>
                                    <li data-path="changsha" data-url="cs" data-city="长沙"><a href="javascript:void(0)">长沙</a></li>
                                    
                                </ul>"""
soup = BeautifulSoup(html,'lxml')
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
cookie = 'Bsksdjd=down_app; route=e028bf8e2ee7f213721872762d23fbc1; ASP.NET_SessionId=uyspthrqh5qlvkmcgvjxid53; sl-session=LxKtMZoXHGiDLeL19Gc88g==; Bsksdjd=down_app; Front_LoginUserKey=85EFE19FA89BC48042B0B15DFB70F3AAC1078FBF2019D8DFFA4051055F57E64A040A36A874273D6E9811D136732B8AB9933B1F99DD7D2D33DD1D2694D7713769AC9CD3994D41A2BBE518E0555C4372A1444C00DDCB87BA262252A6ACE19228EED2E5C2371A83A18269C8DC396A238D918206B6D81D58E5D09A4678F19B15A5D2CFB14D86AF82ED057C116499031335F8185D6B9DDB5C3FE289877C3C55CAE9A10AB3804BB6992771A99240E2D13B880AEAFD9DADB6C62B21543E9DCD827354CB5BA7BEA030B5ECE0'
cities = []
all_data = pd.DataFrame()
for li in soup.select('ul.s_citywindow_main > li'):
    cities.append(
        li.get('data-path')
    )
def Spider(city,page):
    #访问request的参数：url,header,cookie,user agent:请注意 header是一个头接口，应该包含访问者信息。
    url = f"https://www.muniao.com/{city}/null-0-0-0-0-0-0-0-{page}.html?&tn=mn19091015"
    headers = {'User-Agent':UserAgent,'Cookie':cookie}
    resp = requests.get(url,headers=headers)
    html = resp.text #先转化为文本再用lxml转化？转化为什么?
    #解析
    tree = etree.HTML(html)

    #所需内容属性提取 价格图片分数类型
    names = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[1]/a/text()')
    huxing = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[1]/text()')
    kezhus = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[3]/text()')
    prices = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/div[2]/span/text()')
    image_url = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[2]/div[1]/a/img/text()')
    scores = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[2]/div[2]/div[2]/span/text()')
    type = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[2]/text()')
    print(names)

    data = pd.DataFrame({
        '名字': pd.Series(names),
        '户型': pd.Series(huxing),
        '可住': pd.Series(kezhus),
        '价格': pd.Series(prices),
        '图片': pd.Series(image_url),
        '评价': pd.Series(scores),
        '类型': pd.Series(type)
    })
    data['城市'] = city
    return data


for city in cities:
    for page in range(1,11):
        print(f"{city}第{page}页,爬取中...")
        data = Spider(city, page)
        all_data = pd.concat([all_data,data],ignore_index=True)
        time.sleep(3)
all_data.to_csv('data.csv',index = False)

print("All done")