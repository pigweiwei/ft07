#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from datetime import datetime

# 接口 URL（东方财富，获取沪深A股行情）
url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&fields=f3&fltt=2&fs=m:0+t:6,m:0+t:13"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

resp = requests.get(url, headers=headers)
data = resp.json()

# 判断是否成功获取数据
if "data" not in data or "diff" not in data["data"]:
    print("获取行情数据失败，接口返回异常")
    exit(1)

# 解析上涨、下跌家数
diff_list = data["data"]["diff"]
up_count = len([x for x in diff_list if x.get("f3", 0) > 0])
down_count = len([x for x in diff_list if x.get("f3", 0) < 0])

# 输出日志
print(f"上涨家数: {up_count}, 下跌家数: {down_count}")

# 推送到 Server酱
server_key = os.environ.get("SERVERCHAN_KEY")
if not server_key:
    print("未设置 SERVERCHAN_KEY 环境变量")
    exit(1)

title = "A股上涨下跌家数检测"
desp = f"当前上涨家数：{up_count}\n当前下跌家数：{down_count}\n更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

push_url = f"https://12404.push.ft07.com/send/{server_key}.send"
requests.get(push_url, params={"title": title, "desp": desp})
