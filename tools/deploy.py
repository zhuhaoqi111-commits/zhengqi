#!/usr/bin/env python3
"""
部署脚本
"""
import os
import subprocess
import sys

def run_command(cmd, description):
    """运行命令并处理错误"""
    print(f"正在执行: {description}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✓ {description} 完成")
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} 失败: {e}")
        sys.exit(1)

def main():
    print("=== 部署脚本 ===")
    
    # 检查环境变量
    if not os.path.exists(".env"):
        print("警告: 未找到.env文件，请复制envs/.env.example并配置")
        
    # 运行测试
    run_command("python -m pytest tests/", "运行测试")
    
    # 收集静态文件
    run_command("python manage.py collectstatic --noinput", "收集静态文件")
    
    # 运行数据库迁移
    run_command("python manage.py migrate", "运行数据库迁移")
    
    # 重启服务（这里需要根据实际部署环境调整）
    print("\n=== 部署完成 ===")
    print("请根据您的部署环境重启服务")

if __name__ == "__main__":
    main()