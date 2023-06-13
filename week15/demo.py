import requests
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import re
# 定义城市代码和城市名字的映射关系
city_dict = {
    "101010100": "北京",
    "101020100": "上海",
    "101030100": "天津",
    "101040100": "重庆",
    "101050101": "哈尔滨",
    "101060101": "长春",
    "101070101": "沈阳",
    "101080101": "呼和浩特",
    "101090101": "石家庄",
    "101100101": "太原",
    "101110101": "西安",
    "101120101": "济南",
    "101130101": "郑州",
    "101140101": "南京",
    "101150101": "合肥",
    "101160101": "杭州",
    "101170101": "福州",
    "101180101": "南昌",
    "101190101": "武汉",
    "101200101": "长沙",
    "101210101": "广州",
    "101220101": "南宁",
    "101230101": "海口",
    "101240101": "成都",
    "101250101": "贵阳",
    "101260101": "昆明",
    "101270101": "西宁",
    "101280101": "兰州",
    "101290101": "银川",
    "101300101": "西安",
    "101310101": "台北",
    "101320101": "香港",
    "101330101": "澳门"
}

# 定义天气信息获取函数
def get_weather(city_code):
    single_weather = {}
    # 定义天气信息获取的网址
    url1 = f'http://www.weather.com.cn/weather/{city_code}.shtml'
    url2 = f'http://www.weather.com.cn/weather1d/{city_code}.shtml'

    try:
        # 尝试获取第一个网址的天气信息
        response = requests.get(url1)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        weather = soup.find(class_='wea').text.strip()
        temp = soup.find(class_='tem').text.strip()
        #匹配temp中/前面的数字
        temp_high = int(re.findall(r'\d+',temp)[0])
        #返回single_weather
        single_weather['city'] = city_dict[city_code]
        single_weather['weather'] = weather
        single_weather['temp'] = temp
        single_weather['temp_high'] = temp_high
        return single_weather

    except:
        # 如果第一个网址获取失败，则尝试获取第二个网址的天气信息
        try:
            response = requests.get(url2)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            weather = soup.find(class_='wea').text.strip()
            temp = soup.find(class_='tem').text.strip()
            return f'{city_dict[city_code]}天气：{weather}，温度：{temp}'

        except:
            # 如果两个网址都获取失败，则返回获取失败的信息
            return f'{city_dict[city_code]}天气信息获取失败'
print(get_weather('101010100'))