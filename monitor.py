import requests

def fetch_market_stats():
    """
    使用 Tushare 获取A股市场上涨和下跌家数（通过股票数据统计）。
    返回 (rising_count, falling_count)，失败返回 (None, None)
    """
    try:
        # 动态导入 Tushare（无需 token，免费版）
        import tushare as ts
        # 获取当天所有股票的日线数据
        df = ts.get_day_all()
        if df is None or df.empty:
            print("Tushare 返回空数据，可能非交易时间")
            return None, None
        # 计算上涨（pct_change > 0）和下跌（pct_change < 0）家数
        rising_count = len(df[df['changepercent'] > 0])
        falling_count = len(df[df['changepercent'] < 0])
        print(f"原始数据行数: {len(df)}")  # 调试
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
