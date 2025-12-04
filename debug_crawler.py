#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试数据抓取模块 - 查看百度返回的实际HTML内容
"""

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

def debug_baidu_search():
    """调试百度搜索页面结构"""
    
    # 测试关键词
    keywords = ["西昌", "科技", "财经", "人工智能"]
    
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    
    for keyword in keywords:
        print(f"\n=== 调试关键词: {keyword} ===")
        
        # 构建百度新闻搜索URL
        url = f"https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word={keyword}"
        
        try:
            # 发送请求
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"状态码: {response.status_code}")
            print(f"内容长度: {len(response.text)} 字符")
            
            # 检查是否被重定向
            if response.history:
                print("请求被重定向:")
                for resp in response.history:
                    print(f"  {resp.status_code}: {resp.url}")
            
            # 保存HTML内容到文件以便分析
            filename = f"debug_{keyword}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"HTML内容已保存到: {filename}")
            
            # 分析HTML结构
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有h3标签
            h3_tags = soup.find_all('h3')
            print(f"找到 {len(h3_tags)} 个h3标签")
            for i, h3 in enumerate(h3_tags[:5]):  # 只显示前5个
                print(f"  h3[{i}]: {h3.get_text(strip=True)[:50]}...")
            
            # 查找所有a标签
            a_tags = soup.find_all('a')
            print(f"找到 {len(a_tags)} 个a标签")
            
            # 查找新闻相关的链接
            news_links = []
            for a in a_tags:
                href = a.get('href', '')
                text = a.get_text(strip=True)
                if href.startswith('http') and len(text) > 10:
                    news_links.append((text, href))
            
            print(f"找到 {len(news_links)} 个可能的新闻链接")
            for i, (text, href) in enumerate(news_links[:5]):
                print(f"  新闻[{i}]: {text[:30]}... -> {href[:50]}...")
            
            # 查找所有div标签
            div_tags = soup.find_all('div')
            print(f"找到 {len(div_tags)} 个div标签")
            
            # 查找包含新闻的div
            news_divs = []
            for div in div_tags:
                class_attr = div.get('class', [])
                if class_attr and any('news' in str(c).lower() or 'result' in str(c).lower() for c in class_attr):
                    news_divs.append(div)
            
            print(f"找到 {len(news_divs)} 个可能的新闻div")
            
        except Exception as e:
            print(f"请求失败: {e}")

if __name__ == "__main__":
    debug_baidu_search()