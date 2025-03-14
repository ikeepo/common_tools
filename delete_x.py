"""
尚未成功，可能是因为免费账户不支持
"""

import tweepy
from datetime import datetime
import os
from pytz import UTC
import time

# 从环境变量加载 API 密钥
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
API_KEY = os.getenv("X_API_KEY")
API_SECRET = os.getenv("X_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# 检查环境变量是否设置
if not all([BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise ValueError("请确保所有 X API 环境变量都已正确设置！")

# 创建 v2 Client
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

# 指定删除时间起点
CUTOFF_DATE = datetime(2024, 11, 1, tzinfo=UTC)


# 获取并删除推文
def delete_tweets_after_date(cutoff_date):
    try:
        # 获取当前用户 ID
        me = client.get_me().data
        user_id = me.id

        # 使用 Paginator 获取推文
        deleted_count = 0
        paginator = tweepy.Paginator(
            client.get_users_tweets,
            id=user_id,
            tweet_fields=["created_at"],
            max_results=50,  # 减少到 50，降低请求频率
        )

        for page in paginator:
            for tweet in page.data:
                tweet_date = tweet.created_at
                if tweet_date > cutoff_date:
                    try:
                        client.delete_tweet(tweet.id)
                        print(f"已删除推文 (ID: {tweet.id}) 创建时间: {tweet_date}")
                        deleted_count += 1
                        time.sleep(1)  # 每次删除后等待 1 秒
                    except tweepy.TweepyException as e:
                        print(f"删除推文 (ID: {tweet.id}) 失败: {e}")
            print("完成一页处理，等待 5 秒...")
            time.sleep(5)  # 每页数据处理完后等待 5 秒

        print(f"总共删除了 {deleted_count} 条推文")

    except tweepy.TooManyRequests:
        print("遇到速率限制，等待 15 分钟后重试...")
        time.sleep(900)  # 等待 15 分钟（900 秒）
        delete_tweets_after_date(cutoff_date)  # 递归重试
    except Exception as e:
        print(f"发生错误: {e}")


# 执行删除
if __name__ == "__main__":
    print(f"正在删除 {CUTOFF_DATE} 之后的推文...")
    delete_tweets_after_date(CUTOFF_DATE)
