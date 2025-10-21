import requests

def fetch_market_stats():
    """
    使用 Sina Finance API 获取A股市场上涨和下跌家数。
    返回 (rising_count, falling_count)，失败返回 (None, None)
    """
    try:
        url = "http://hq.sinajs.cn/list=s_sh000001,s_sz399001"  # 上证+深证市场统计
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.text
        print(f"API 响应: {data}")  # 调试用

        # 示例响应: var hq_str_s_sh000001="上证指数,3000.12,...,上涨家数:1500,下跌家数:1200";
        parts = data.split(';')
        rising_count = None
        falling_count = None
        for part in parts:
            if '上涨家数' in part and '下跌家数' in part:
                # 假设格式：上涨家数:XXXX,下跌家数:YYYY
                rising_str = part.split('上涨家数:')[1].split(',')[0]
                falling_str = part.split('下跌家数:')[1].split('"')[0]
                rising_count = int(rising_str)
                falling_count = int(falling_str)
                break
        if rising_count is None or falling_count is None:
            print("未找到涨跌家数数据")
            return None, None
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
