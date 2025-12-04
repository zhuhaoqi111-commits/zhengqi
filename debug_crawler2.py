#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试数据抓取模块 - 检查百度返回的响应头信息
"""

import requests
import gzip
import io

def debug_baidu_response():
    """调试百度搜索响应信息"""
    
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
        print(f"响应头:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        # 检查内容编码
        print(f"\n内容编码: {response.encoding}")
        print(f"内容类型: {response.headers.get('content-type', '未知')}")
        
        # 尝试解码内容
        content_type = response.headers.get('content-type', '')
        
        if 'gzip' in content_type or response.content.startswith(b'\x1f\x8b'):
            print("检测到gzip压缩内容")
            try:
                decompressed = gzip.decompress(response.content)
                print(f"解压后长度: {len(decompressed)} 字节")
                
                # 保存解压后的内容
                with open('debug_西昌_decompressed.html', 'wb') as f:
                    f.write(decompressed)
                print("解压内容已保存到: debug_西昌_decompressed.html")
                
                # 查看解压内容的前500字符
                try:
                    text_content = decompressed.decode('utf-8', errors='ignore')
                    print(f"\n解压内容前500字符:\n{text_content[:500]}")
                except:
                    print("无法解码为UTF-8文本")
            except Exception as e:
                print(f"解压失败: {e}")
        
        # 尝试直接解码响应内容
        try:
            text_content = response.content.decode('utf-8', errors='ignore')
            print(f"\n原始内容前500字符:\n{text_content[:500]}")
        except Exception as e:
            print(f"直接解码失败: {e}")
            
        # 尝试其他编码
        encodings = ['gbk', 'gb2312', 'utf-8', 'latin-1']
        for encoding in encodings:
            try:
                text_content = response.content.decode(encoding, errors='ignore')
                if '百度' in text_content or '新闻' in text_content:
                    print(f"\n使用{encoding}编码成功，包含百度或新闻关键词")
                    print(f"内容前300字符:\n{text_content[:300]}")
                    break
            except:
                continue
                
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    debug_baidu_response()