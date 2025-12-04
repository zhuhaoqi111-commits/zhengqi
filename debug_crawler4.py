#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试数据抓取模块 - 检查百度返回的实际内容
"""

import requests
from bs4 import BeautifulSoup

def debug_baidu_content():
    """调试百度搜索实际内容"""
    
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'identity',  # 禁用压缩
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
        print(f"最终URL: {response.url}")
        
        # 检查重定向历史
        if response.history:
            print("重定向历史:")
            for resp in response.history:
                print(f"  {resp.status_code}: {resp.url}")
        
        # 保存原始内容
        with open('debug_西昌_raw.html', 'wb') as f:
            f.write(response.content)
        print("原始内容已保存到: debug_西昌_raw.html")
        
        # 查看内容前1000字符
        try:
            text_content = response.content.decode('utf-8', errors='ignore')
            print(f"\n内容前1000字符:\n{text_content[:1000]}")
        except Exception as e:
            print(f"解码失败: {e}")
            
        # 尝试解析HTML
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 检查标题
            title = soup.find('title')
            if title:
                print(f"\n页面标题: {title.get_text()}")
            
            # 检查是否有错误信息
            error_divs = soup.find_all('div', class_=True)
            for div in error_divs:
                class_attr = div.get('class', [])
                class_str = ' '.join(class_attr)
                if 'error' in class_str.lower() or 'msg' in class_str.lower():
                    text = div.get_text(strip=True)
                    if text:
                        print(f"错误信息: {text}")
            
            # 检查是否有验证码
            captcha_elements = soup.find_all(text=lambda t: '验证码' in t if t else False)
            if captcha_elements:
                print("检测到验证码页面")
                
            # 检查是否有重定向脚本
            scripts = soup.find_all('script')
            for script in scripts:
                script_text = script.get_text()
                if 'location.href' in script_text or 'window.location' in script_text:
                    print("检测到重定向脚本")
                    print(f"脚本内容: {script_text[:200]}")
                    
        except Exception as e:
            print(f"HTML解析失败: {e}")
            
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    debug_baidu_content()