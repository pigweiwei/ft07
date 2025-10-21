import requests

def fetch_market_stats():
    """
    使用 Sina Finance API 获取A股市场上涨和下跌家数。
    返回 (rising_count, falling_count)，失败返回 (None, None)
    """
    try:
        # Sina Finance 市场概览 API（示例，需替换为实际涨跌家数接口）
        # 假设使用 http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_pos_zs.php
        url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_pos_zs.php?code=000001"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # 提取上涨和下跌家数（根据实际 JSON 结构调整）
        rising_count = int(data['result'][0]['data']['up_count'])
        falling_count = int(data['result'][0]['data']['down_count'])
        return rising_count, falling_count
    except Exception as e:
        print(f"抓取失败: {e}")
        return None, None

def send_notification(rising, falling):
    """
    通过 ServerChan API 推送通知，使用 title 和 desp 参数
    """
    api_url = "https://12404.push.ft07.com/send/sctp12404t9hn7aimbwueu29q2cnvxkl.send"
    title = "市场警报"
    desp = f"上涨家数={rising}，下跌家数={falling}"
    params = {'title': title, 'desp': desp}
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        print(f"推送成功: {title} - {desp}")
    except Exception as e:
        print(f"推送失败: {e}")

def main():
    rising, falling = fetch_market_stats()
    if rising is not None and falling is not None:
        print(f"当前：上涨={rising}，下跌={falling}")
        # 测试：强制推送一次，确保通知工作
        send_notification(rising, falling)
        # 正式条件（取消注释后使用）
        # if rising > 3000 or falling > 3000:
        #     send_notification(rising, falling)
    else:
        print("数据抓取失败")

if __name__ == "__main__":
    main()
