#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试数据抓取模块 - 正确处理gzip压缩内容
"""

import requests
import gzip
import io
from bs4 import BeautifulSoup

def debug_baidu_gzip():
    """调试百度搜索gzip压缩内容"""
    
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
    
    keyword = "西昌"
    
    # 构建百度新闻搜索URL
    url = f"https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word={keyword}"
    
    try:
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.content)} 字节")
        
        # 检查是否是gzip压缩
        if response.headers.get('content-encoding') == 'gzip' or response.content[:2] == b'\x1f\x8b':
            print("检测到gzip压缩内容")
            
            # 方法1: 使用gzip模块解压
            try:
                decompressed = gzip.decompress(response.content)
                print(f"方法1解压后长度: {len(decompressed)} 字节")
                
                # 保存解压后的内容
                with open('debug_西昌_gzip.html', 'wb') as f:
                    f.write(decompressed)
                print("解压内容已保存到: debug_西昌_gzip.html")
                
                # 解析HTML
                soup = BeautifulSoup(decompressed, 'html.parser')
                
                # 查找新闻标题
                titles = soup.find_all('h3')
                print(f"找到 {len(titles)} 个h3标题")
                for i, title in enumerate(titles[:5]):
                    print(f"  标题[{i}]: {title.get_text(strip=True)[:50]}")
                
                # 查找新闻链接
                links = soup.find_all('a')
                print(f"找到 {len(links)} 个链接")
                
                # 查找可能的新闻链接
                news_links = []
                for link in links:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    if href.startswith('http') and len(text) > 10:
                        news_links.append((text, href))
                
                print(f"找到 {len(news_links)} 个可能的新闻链接")
                for i, (text, href) in enumerate(news_links[:5]):
                    print(f"  新闻[{i}]: {text[:30]} -> {href[:50]}")
                
                # 查找新闻容器
                divs = soup.find_all('div')
                print(f"找到 {len(divs)} 个div")
                
                # 查找包含新闻的div
                for div in divs[:20]:
                    class_attr = div.get('class', [])
                    if class_attr:
                        class_str = ' '.join(class_attr)
                        if 'news' in class_str.lower() or 'result' in class_str.lower():
                            print(f"  新闻div: {class_str}")
                            text = div.get_text(strip=True)
                            if len(text) > 50:
                                print(f"    内容: {text[:100]}...")
                
            except Exception as e:
                print(f"方法1解压失败: {e}")
        
        # 方法2: 使用requests自动解压
        try:
            # 重新发送请求，禁用自动解压
            headers_no_gzip = headers.copy()
            headers_no_gzip['Accept-Encoding'] = 'identity'
            
            response_no_gzip = requests.get(url, headers=headers_no_gzip, timeout=10)
            
            print(f"\n方法2 - 禁用gzip后内容长度: {len(response_no_gzip.content)} 字节")
            
            # 解析HTML
            soup = BeautifulSoup(response_no_gzip.content, 'html.parser')
            
            # 查找新闻标题
            titles = soup.find_all('h3')
            print(f"找到 {len(titles)} 个h3标题")
            for i, title in enumerate(titles[:5]):
                print(f"  标题[{i}]: {title.get_text(strip=True)[:50]}")
            
        except Exception as e:
            print(f"方法2失败: {e}")
            
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    debug_baidu_gzip()