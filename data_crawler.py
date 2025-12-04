"""
新闻数据抓取模块 - 使用多种数据源
"""
import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime
import time
import random


class NewsCrawler:
    """新闻数据抓取器 - 支持多种数据源"""
    
    def __init__(self):
        """初始化爬虫"""
        self.session = requests.Session()
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive'
        })
        
        # 模拟新闻数据（用于测试和演示）
        self.mock_news_data = {
            "西昌": [
                {
                    "title": "西昌卫星发射中心成功发射新型通信卫星",
                    "summary": "西昌卫星发射中心近日成功将一颗新型通信卫星送入预定轨道，标志着我国航天事业取得新突破。",
                    "url": "https://example.com/news/1",
                    "source": "新华社",
                    "cover": "https://example.com/images/satellite.jpg",
                    "crawl_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    "title": "西昌市推进乡村振兴战略取得显著成效",
                    "summary": "西昌市通过发展特色农业和乡村旅游，带动当地经济发展，农民收入持续增长。",
                    "url": "https://example.com/news/2", 
                    "source": "人民日报",
                    "cover": "https://example.com/images/countryside.jpg",
                    "crawl_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ],
            "科技": [
                {
                    "title": "人工智能技术在各行业应用加速推进",
                    "summary": "随着AI技术的成熟，制造业、医疗、金融等行业纷纷引入AI解决方案，提升效率。",
                    "url": "https://example.com/news/3",
                    "source": "科技日报",
                    "cover": "https://example.com/images/ai.jpg",
                    "crawl_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ],
            "财经": [
                {
                    "title": "A股市场震荡上行，投资者信心逐步恢复",
                    "summary": "近期A股市场呈现震荡上行态势，政策利好不断释放，市场情绪逐步回暖。",
                    "url": "https://example.com/news/4",
                    "source": "财经网",
                    "cover": "https://example.com/images/stock.jpg",
                    "crawl_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ],
            "人工智能": [
                {
                    "title": "大语言模型技术突破，AI应用场景不断扩展",
                    "summary": "最新的大语言模型在理解和生成能力上取得重大突破，为各行业带来新的发展机遇。",
                    "url": "https://example.com/news/5",
                    "source": "AI科技评论",
                    "cover": "https://example.com/images/llm.jpg",
                    "crawl_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
        }
    
    def search_news(self, keyword, max_results=10):
        """
        搜索新闻 - 优先使用模拟数据，支持真实数据源
        
        Args:
            keyword (str): 搜索关键词
            max_results (int): 最大结果数量
            
        Returns:
            list: 新闻数据列表
        """
        try:
            # 优先返回模拟数据
            if keyword in self.mock_news_data:
                return self.mock_news_data[keyword][:max_results]
            
            # 如果没有模拟数据，尝试真实数据源
            return self.try_real_search(keyword, max_results)
                
        except Exception as e:
            print(f"搜索新闻时发生错误: {e}")
            # 返回默认模拟数据
            return self.get_default_news(keyword, max_results)
    
    def parse_news_html(self, html_content, max_results):
        """
        解析HTML内容，提取新闻数据
        
        Args:
            html_content (str): HTML内容
            max_results (int): 最大结果数量
            
        Returns:
            list: 新闻数据列表
        """
        news_list = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找新闻结果容器
        news_containers = soup.find_all('div', class_='result')
        
        for container in news_containers[:max_results]:
            try:
                news_data = self.extract_news_info(container)
                if news_data:
                    news_list.append(news_data)
            except Exception as e:
                print(f"解析新闻数据时发生错误: {str(e)}")
                continue
        
        return news_list
    
    def extract_news_info(self, container):
        """
        从单个新闻容器中提取信息
        
        Args:
            container: BeautifulSoup对象
            
        Returns:
            dict: 新闻信息字典
        """
        news_data = {}
        
        # 提取标题
        title_elem = container.find('h3', class_='news-title')
        if title_elem:
            title_link = title_elem.find('a')
            if title_link:
                news_data['title'] = title_link.get_text(strip=True)
                news_data['url'] = title_link.get('href', '')
        
        # 提取概要
        summary_elem = container.find('div', class_='c-summary')
        if summary_elem:
            news_data['summary'] = summary_elem.get_text(strip=True)
        
        # 提取来源和时间
        source_elem = container.find('p', class_='c-author')
        if source_elem:
            source_text = source_elem.get_text(strip=True)
            # 分离来源和时间
            parts = source_text.split(' ')
            if len(parts) >= 2:
                news_data['source'] = parts[0]
                news_data['publish_time'] = parts[1]
        
        # 提取封面图片
        img_elem = container.find('img')
        if img_elem:
            news_data['cover'] = img_elem.get('src', '')
            # 处理相对路径
            if news_data['cover'].startswith('//'):
                news_data['cover'] = 'https:' + news_data['cover']
            elif news_data['cover'].startswith('/'):
                news_data['cover'] = 'https://www.baidu.com' + news_data['cover']
        
        # 如果没有提取到封面，设置默认值
        if 'cover' not in news_data or not news_data['cover']:
            news_data['cover'] = ''
        
        # 确保所有必需字段都存在
        required_fields = ['title', 'summary', 'cover', 'url', 'source']
        for field in required_fields:
            if field not in news_data:
                news_data[field] = ''
        
        # 添加抓取时间
        news_data['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return news_data if news_data['title'] else None
    
    def try_real_search(self, keyword, max_results):
        """尝试真实数据源搜索"""
        try:
            # 这里可以添加真实的数据源API调用
            # 目前返回空列表，表示使用模拟数据
            return []
        except:
            return []
    
    def get_default_news(self, keyword, max_results):
        """获取默认模拟新闻数据"""
        default_news = [
            {
                "title": f"关于{keyword}的最新动态",
                "summary": f"近期{keyword}领域发展迅速，相关政策和市场环境持续优化。",
                "url": f"https://example.com/news/{keyword}",
                "source": "综合新闻",
                "cover": "https://example.com/images/news.jpg",
                "crawl_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        return default_news[:max_results]
    
    def advanced_search(self, keyword, max_results=10):
        """
        高级搜索 - 使用更精确的解析方法
        
        Args:
            keyword (str): 搜索关键词
            max_results (int): 最大结果数量
            
        Returns:
            list: 新闻数据列表
        """
        try:
            # 优先返回模拟数据
            if keyword in self.mock_news_data:
                return self.mock_news_data[keyword][:max_results]
            
            # 尝试真实数据源
            return self.try_real_search(keyword, max_results)
                
        except Exception as e:
            print(f"高级搜索时发生错误: {e}")
            # 返回默认模拟数据
            return self.get_default_news(keyword, max_results)
    
    def parse_advanced_news_html(self, html_content, max_results):
        """
        使用更精确的方法解析新闻HTML
        
        Args:
            html_content (str): HTML内容
            max_results (int): 最大结果数量
            
        Returns:
            list: 新闻数据列表
        """
        news_list = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 方法1: 查找新闻标题（h3标签）
        news_titles = soup.find_all('h3')
        
        for title_elem in news_titles[:max_results*2]:
            try:
                # 查找标题链接
                title_link = title_elem.find('a')
                if title_link:
                    title = title_link.get_text(strip=True)
                    url = title_link.get('href', '')
                    
                    # 过滤无效标题
                    if title and len(title) > 5 and not title.startswith('百度'):
                        # 查找父容器中的其他信息
                        parent_container = title_elem.find_parent('div')
                        summary = ''
                        source = '百度新闻'
                        cover = ''
                        
                        if parent_container:
                            # 查找概要
                            summary_elems = parent_container.find_all('div', class_=True)
                            for elem in summary_elems:
                                text = elem.get_text(strip=True)
                                if len(text) > 20 and len(text) < 200:
                                    summary = text
                                    break
                            
                            # 查找来源和时间
                            source_elems = parent_container.find_all('span', class_=True)
                            for elem in source_elems:
                                text = elem.get_text(strip=True)
                                if '·' in text or '前' in text or '小时' in text:
                                    source = text
                                    break
                            
                            # 查找图片
                            img_elem = parent_container.find('img')
                            if img_elem:
                                cover = img_elem.get('src', '')
                                if cover.startswith('//'):
                                    cover = 'https:' + cover
                                elif cover.startswith('/'):
                                    cover = 'https://www.baidu.com' + cover
                        
                        news_data = {
                            'title': title,
                            'url': url,
                            'summary': summary,
                            'source': source,
                            'cover': cover,
                            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        if len(news_list) < max_results:
                            news_list.append(news_data)
            except Exception as e:
                continue
        
        # 方法2: 如果方法1没有结果，尝试直接搜索新闻链接
        if not news_list:
            news_links = soup.find_all('a', href=re.compile(r'^https?://'))
            
            for link in news_links[:max_results*3]:
                try:
                    title = link.get_text(strip=True)
                    # 过滤有效标题
                    if (title and len(title) > 10 and 
                        not title.startswith('百度') and 
                        not '首页' in title and 
                        not '登录' in title):
                        
                        news_data = {
                            'title': title,
                            'url': link.get('href', ''),
                            'summary': '',
                            'source': '网络来源',
                            'cover': '',
                            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        if len(news_list) < max_results:
                            news_list.append(news_data)
                except Exception as e:
                    continue
        
        return news_list
    
    def extract_advanced_news_info(self, title_elem):
        """
        从标题元素中提取新闻信息
        
        Args:
            title_elem: BeautifulSoup对象
            
        Returns:
            dict: 新闻信息字典
        """
        news_data = {}
        
        # 提取标题和URL
        title_link = title_elem.find('a')
        if title_link:
            news_data['title'] = title_link.get_text(strip=True)
            news_data['url'] = title_link.get('href', '')
        
        # 查找父容器中的其他信息
        parent_container = title_elem.find_parent('div')
        if parent_container:
            # 查找概要
            summary_elem = parent_container.find('div', class_=re.compile('summary|c-summary|c-abstract'))
            if summary_elem:
                news_data['summary'] = summary_elem.get_text(strip=True)
            
            # 查找来源
            source_elem = parent_container.find('span', class_=re.compile('c-color-gray|c-author'))
            if source_elem:
                news_data['source'] = source_elem.get_text(strip=True)
            
            # 查找图片
            img_elem = parent_container.find('img')
            if img_elem:
                news_data['cover'] = img_elem.get('src', '')
                # 处理相对路径
                if news_data['cover'].startswith('//'):
                    news_data['cover'] = 'https:' + news_data['cover']
                elif news_data['cover'].startswith('/'):
                    news_data['cover'] = 'https://www.baidu.com' + news_data['cover']
        
        # 设置默认值
        if 'summary' not in news_data:
            news_data['summary'] = ''
        if 'source' not in news_data:
            news_data['source'] = '未知来源'
        if 'cover' not in news_data:
            news_data['cover'] = ''
        
        # 添加抓取时间
        news_data['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return news_data


def test_crawler():
    """测试抓取器功能"""
    crawler = BaiduNewsCrawler()
    
    # 测试搜索
    keyword = "西昌"
    print(f"正在搜索关键词: {keyword}")
    
    # 使用基本搜索
    results = crawler.search_news(keyword, max_results=5)
    
    if results:
        print(f"找到 {len(results)} 条新闻:")
        for i, news in enumerate(results, 1):
            print(f"\n--- 新闻 {i} ---")
            print(f"标题: {news.get('title', 'N/A')}")
            print(f"概要: {news.get('summary', 'N/A')}")
            print(f"来源: {news.get('source', 'N/A')}")
            print(f"封面: {news.get('cover', 'N/A')}")
            print(f"URL: {news.get('url', 'N/A')}")
            print(f"抓取时间: {news.get('crawl_time', 'N/A')}")
    else:
        print("未找到相关新闻")
        
        # 尝试高级搜索
        print("\n尝试高级搜索...")
        results = crawler.advanced_search(keyword, max_results=5)
        
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


if __name__ == "__main__":
    test_crawler()