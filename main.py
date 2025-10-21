import akshare as ak
import requests

def fetch_market_stats():
    """
    使用 AKShare 获取A股市场上涨和下跌家数。
    返回 (rising_count, falling_count)，失败返回 (None, None)
    """
    try:
        # 获取A股市场实时概览
        df = ak.stock_market_activity_sina()
        # 提取上涨家数和下跌家数
        rising_count = int(df.loc[df['item'] == '上涨家数', 'value'].iloc[0])
        falling_count = int(df.loc[df['item'] == '下跌家数', 'value'].iloc[0])
        return rising_count, falling_count
    except Exception as e:
        print(f"抓取失败: {e}")
        return None, None

def send_notification(rising, falling):
    """
    通过 API 推送通知，假设 GET 请求，参数为 message
    """
    api_url = "https://12404.push.ft07.com/send/sctp12404t9hn7aimbwueu29q2cnvxkl.send"
    message = f"市场警报：上涨家数={rising}，下跌家数={falling}"
    params = {'message': message}
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        print(f"推送成功: {message}")
    except Exception as e:
        print(f"推送失败: {e}")

def main():
    """
    主逻辑：检查涨跌家数，满足条件时推送
    """
    rising, falling = fetch_market_stats()
    if rising is not None and falling is not None:
        print(f"当前：上涨={rising}，下跌={falling}")
        if rising > 3000 or falling > 3000:
            send_notification(rising, falling)
    else:
        print("数据抓取失败")

if __name__ == "__main__":
    main()
