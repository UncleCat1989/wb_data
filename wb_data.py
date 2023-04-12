#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 19:54:59 2023

@author: DHY
"""
import numpy as np
from matplotlib.animation import FuncAnimation
import requests
import matplotlib.pyplot as plt
from IPython.display import display
# World Bank API 指标字典
INDICATORS = {
    "1": "NY.GDP.MKTP.CD",    # GDP
    "2": "NY.GDP.PCAP.CD",    # 平均GDP
    "3": "SI.POV.NAHC",       # 贫困线以下人口
    "4": "FP.CPI.TOTL.ZG",    # 通胀率
    "5": "SL.UEM.TOTL.ZS",    # 失业率
    "6": "GC.DOD.TOTL.GD.ZS", # 政府债务
    "7": "SP.POP.TOTL",       # 总人口
    "8": "SP.POP.GROW",       # 人口增长率
    "9": "SI.POV.GINI"        # 基尼系数
}

# def get_data(country, indicator, start_year, end_year):
#     url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start_year}:{end_year}&format=json"
#     response = requests.get(url)
#     data = response.json()
#     return data

def get_data(country, indicator, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start_year}:{end_year}&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    
    # 创建一个字典，将年份映射到值
    year_value_map = {str(year): None for year in range(start_year, end_year + 1)}
    
    for item in data[1]:
        year = item['date']
        value = item['value']
        year_value_map[year] = value
    
    # 将字典转换为按年份排序的元组列表
    sorted_data = sorted(year_value_map.items(), key=lambda x: x[0])
    
    return data[0], sorted_data


from IPython.display import HTML

def plot_data(country1, country2, indicator_id, start_year, end_year):
    indicator = INDICATORS[indicator_id]
    data1 = get_data(country1, indicator, start_year, end_year)
    data2 = get_data(country2, indicator, start_year, end_year)
    if data1 is None or data2 is None:
        print("无法获取一个或两个国家的数据。请确保国家代码和指标编号正确。")
        return

    years = [int(year) for year in range(start_year, end_year + 1)]
    values1 = [item[1] for item in data1[1]]
    values2 = [item[1] for item in data2[1]]



    fig, ax = plt.subplots()

    def update(num):
        ax.clear()
        ax.plot(years[:num + 1], values1[:num + 1], label=country1.upper(), marker='o')
        ax.plot(years[:num + 1], values2[:num + 1], label=country2.upper(), marker='o')
        ax.legend()
        ax.set_xlabel("year")
        ax.set_ylabel("value")
        ax.set_title(f"{country1.upper()} and {country2.upper()} 's {indicator_id} comparison ({start_year}-{end_year})")
        ax.set_xlim(start_year, end_year)
        ax.set_ylim(min(filter(None, values1)), max(filter(None, values1 + values2)))

    ani = FuncAnimation(fig, update, frames=len(years), interval=500, repeat=False)
    with open('animation.html', 'w') as f:
        f.write(ani.to_jshtml())
    # 显示动画
    plt.close(fig)  # 关闭额外的空白图像
    print("Years: ", years)
    print(f"{country1.upper()} values: ", values1)
    print(f"{country2.upper()} values: ", values2)

    return HTML(ani.to_jshtml())

   


#静态输出图片
# def plot_data(country1, country2, indicator_id, start_year, end_year):
#     indicator = INDICATORS[indicator_id]
#     data1 = get_data(country1, indicator, start_year, end_year)
#     data2 = get_data(country2, indicator, start_year, end_year)

#     years = [int(year) for year in range(start_year, end_year + 1)]
#     values1 = [item['value'] for item in reversed(data1[1])]
#     values2 = [item['value'] for item in reversed(data2[1])]

#     plt.plot(years, values1, label=country1.upper())
#     plt.plot(years, values2, label=country2.upper())

#     plt.xlabel("year")
#     plt.ylabel("value")
#     plt.title(f"{country1.upper()} and {country2.upper()} 's {indicator_id} comparison({start_year}-{end_year})")
#     plt.legend()

#     plt.show()


if __name__ == "__main__":
    country1 = input("请输入第一个国家的代码：")
    country2 = input("请输入第二个国家的代码：")
    indicator_id = input("请输入要比较的指标编号：")
    start_year = int(input("请输入开始年份："))
    end_year = int(input("请输入结束年份："))
    
    display(plot_data(country1, country2, indicator_id, start_year, end_year))
    #plot_data(country1, country2, indicator_id, start_year, end_year)
