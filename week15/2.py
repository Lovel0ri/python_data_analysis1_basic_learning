import requests
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

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
        return f'{city_dict[city_code]}天气：{weather}，温度：{temp}'

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

# 定义永久化存储函数
def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# 调用函数获取天气信息
weather_data = {}
for city_code in city_dict.keys():
    weather_data[city_dict[city_code]] = get_weather(city_code)

# 将天气信息永久化存储到文件中
save_to_file(weather_data, 'weather.json')

# 从文件中读取天气信息
with open('weather.json', 'r', encoding='utf-8') as f:
    weather_data = json.load(f)

# 打印天气信息
for city, weather in weather_data.items():
    print(weather)

# 定义归并排序函数
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][1] > right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result += left[i:]
    result += right[j:]

    return result

# 对各省份省会城市的温度进行排序
sorted_data = {}
for province in sorted_data:
    city_data = sorted_data[province]
    sorted_city_data = merge_sort(list(city_data.items()))
    sorted_data[province] = sorted_city_data

# 定义可视化函数
def visualize(data):
    fig, axs = plt.subplots(len(data), figsize=(8, 8))

    for i, province in enumerate(data):
        city_data = data[province]

        # 提取今天和明天的温度数据
        today_temp = city_data[0][1][0]
        tomorrow_temp = city_data[0][1][1]

        # 计算平均温度并判断升高、降低或不变
        avg_temp = np.mean([today_temp, tomorrow_temp])
        if today_temp > tomorrow_temp:
            change = '降低'
        elif today_temp < tomorrow_temp:
            change = '升高'
        else:
            change = '不变'

        # 绘制柱状图
        axs[i].bar(['今天', '明天'], [today_temp, tomorrow_temp])
        axs[i].set_title(f'{province} ({change}，平均温度：{avg_temp:.1f}℃)')

    plt.tight_layout()
    plt.savefig('temperature.png')

# 对各省份省会城市今明两日的平均气温变化进行可视化分析

