#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 19:54:59 2023

@author: DHY
"""

import requests
import matplotlib.pyplot as plt

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

def get_data(country, indicator, start_year, end_year):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    data = response.json()
    return data

def plot_data(country1, country2, indicator_id, start_year, end_year):
    indicator = INDICATORS[indicator_id]
    data1 = get_data(country1, indicator, start_year, end_year)
    data2 = get_data(country2, indicator, start_year, end_year)

    years = [int(year) for year in range(start_year, end_year + 1)]
    values1 = [item['value'] for item in reversed(data1[1])]
    values2 = [item['value'] for item in reversed(data2[1])]

    plt.plot(years, values1, label=country1.upper())
    plt.plot(years, values2, label=country2.upper())

    plt.xlabel("年份")
    plt.ylabel("指标值")
    plt.title(f"{country1.upper()} 和 {country2.upper()} 的 {indicator_id} 指标比较 ({start_year}-{end_year})")
    plt.legend()

    plt.show()


if __name__ == "__main__":
    country1 = input("请输入第一个国家的代码：")
    country2 = input("请输入第二个国家的代码：")
    indicator_id = input("请输入要比较的指标编号：")
    start_year = int(input("请输入开始年份："))
    end_year = int(input("请输入结束年份："))

    plot_data(country1, country2, indicator_id, start_year, end_year)
