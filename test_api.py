import requests
import json

def test_crawler_api():
    """测试数据抓取API"""
    url = "http://127.0.0.1:5000/api/crawler/search"
    
    # 测试数据
    test_data = {
        "keyword": "西昌",
        "max_results": 3
    }
    
    try:
        response = requests.post(url, json=test_data)
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nAPI调用成功: {data.get('message', '')}")
            print(f"返回数据条数: {len(data.get('data', []))}")
            
            # 显示新闻数据
            for i, news in enumerate(data.get('data', []), 1):
                print(f"\n--- 新闻 {i} ---")
                print(f"标题: {news.get('title', '')}")
                print(f"概要: {news.get('summary', '')}")
                print(f"来源: {news.get('source', '')}")
                print(f"URL: {news.get('url', '')}")
                print(f"封面: {news.get('cover', '')}")
                print(f"抓取时间: {news.get('crawl_time', '')}")
        else:
            print(f"API调用失败: {response.text}")
            
    except Exception as e:
        print(f"测试过程中发生错误: {e}")

if __name__ == "__main__":
    test_crawler_api()