"""
测试数据抓取模块的独立脚本
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_crawler import NewsCrawler

def test_crawler():
    """测试抓取器功能"""
    print("=== 测试百度新闻数据抓取模块 ===\n")
    
    crawler = NewsCrawler()
    
    # 测试关键词列表
    test_keywords = ["西昌", "科技", "财经", "人工智能"]
    
    for keyword in test_keywords:
        print(f"\n正在搜索关键词: {keyword}")
        print("-" * 50)
        
        # 使用基本搜索
        results = crawler.search_news(keyword, max_results=3)
        
        if results:
            print(f"基本搜索找到 {len(results)} 条新闻:")
            for i, news in enumerate(results, 1):
                print(f"\n--- 新闻 {i} ---")
                print(f"标题: {news.get('title', 'N/A')}")
                print(f"概要: {news.get('summary', 'N/A')}")
                print(f"来源: {news.get('source', 'N/A')}")
                print(f"封面: {news.get('cover', 'N/A')}")
                print(f"URL: {news.get('url', 'N/A')}")
                print(f"抓取时间: {news.get('crawl_time', 'N/A')}")
        else:
            print("基本搜索未找到相关新闻")
            
            # 尝试高级搜索
            print("\n尝试高级搜索...")
            results = crawler.advanced_search(keyword, max_results=3)
            
            if results:
                print(f"高级搜索找到 {len(results)} 条新闻:")
                for i, news in enumerate(results, 1):
                    print(f"\n--- 新闻 {i} ---")
                    print(f"标题: {news.get('title', 'N/A')}")
                    print(f"概要: {news.get('summary', 'N/A')}")
                    print(f"来源: {news.get('source', 'N/A')}")
                    print(f"封面: {news.get('cover', 'N/A')}")
                    print(f"URL: {news.get('url', 'N/A')}")
                    print(f"抓取时间: {news.get('crawl_time', 'N/A')}")
            else:
                print("高级搜索也未找到相关新闻")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    test_crawler()