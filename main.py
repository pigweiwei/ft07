import akshare as ak  # 如果环境不支持，跳到下面备选
import requests

def fetch_market_stats():
    try:
        df = ak.stock_market_activity_sina()
        rising_count = int(df.loc[df['item'] == '上涨家数', 'value'].iloc[0])
        falling_count = int(df.loc[df['item'] == '下跌家数', 'value'].iloc[0])
        return rising_count, falling_count
    except Exception as e:
        print(f"抓取失败: {e}")
        return None, None

def send_notification(rising, falling):
    api_url = "https://12404.push.ft07.com/send/sctp12404t9hn7aimbwueu29q2cnvxkl.send"
    title = "市场警报"  # ServerChan 需要 title
    desp = f"上涨家数={rising}，下跌家数={falling}"  # desp 为内容
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
        # 测试：强制推送一次，无论条件
        send_notification(rising, falling)
        # 正式条件：if rising > 3000 or falling > 3000:
        #     send_notification(rising, falling)
    else:
        print("数据抓取失败")

if __name__ == "__main__":
    main()
